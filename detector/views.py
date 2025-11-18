import os
from typing import Generator, Optional, Any, Dict, List
import cv2  # type: ignore
import numpy as np  # type: ignore
import uuid
from datetime import datetime
from django.http import StreamingHttpResponse, JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PersonCountEvent, PersonTracking

# Variable global para contador
people_count: int = 0
current_event_id: Optional[str] = None
last_saved_count: int = -1

# Control de cámara
camera_active: bool = False
camera_instance: Optional[Any] = None

# Rutas del modelo MobileNet-SSD
BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR: str = os.path.join(BASE_DIR, 'models')
PROTOTXT: str = os.path.join(MODEL_DIR, 'MobileNetSSD_deploy.prototxt')
CAFFEMODEL: str = os.path.join(MODEL_DIR, 'MobileNetSSD_deploy.caffemodel')

# Clase "person" en MobileNet-SSD (índice 15)
CLASS_PERSON: int = 15

# ============================================
# VISTAS DE AUTENTICACIÓN
# ============================================

def login_view(request: HttpRequest) -> HttpResponse:
    """Vista para iniciar sesión"""
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username: str = request.POST.get('username', '')
        password: str = request.POST.get('password', '')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'detector/login.html', {
                'error': 'Usuario o contraseña incorrectos'
            })
    
    return render(request, 'detector/login.html')

def register_view(request: HttpRequest) -> HttpResponse:
    """Vista para registrar nuevo usuario"""
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username: str = request.POST.get('username', '')
        email: str = request.POST.get('email', '')
        password1: str = request.POST.get('password1', '')
        password2: str = request.POST.get('password2', '')
        
        # Validaciones
        if not username or not password1 or not password2:
            return render(request, 'detector/register.html', {
                'error': 'Todos los campos obligatorios deben ser completados',
                'username': username,
                'email': email
            })
        
        if password1 != password2:
            return render(request, 'detector/register.html', {
                'error': 'Las contraseñas no coinciden',
                'username': username,
                'email': email
            })
        
        if len(password1) < 8:
            return render(request, 'detector/register.html', {
                'error': 'La contraseña debe tener al menos 8 caracteres',
                'username': username,
                'email': email
            })
        
        if User.objects.filter(username=username).exists():
            return render(request, 'detector/register.html', {
                'error': 'El nombre de usuario ya existe',
                'username': '',
                'email': email
            })
        
        # Crear usuario
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            # Redirigir a login con mensaje de éxito
            return render(request, 'detector/login.html', {
                'success': 'Cuenta creada exitosamente. Por favor inicia sesión.'
            })
        except Exception as e:
            return render(request, 'detector/register.html', {
                'error': f'Error al crear la cuenta: {str(e)}',
                'username': username,
                'email': email
            })
    
    return render(request, 'detector/register.html')

def logout_view(request: HttpRequest) -> HttpResponse:
    """Vista para cerrar sesión"""
    logout(request)
    return redirect('login')

# ============================================
# VISTAS PRINCIPALES (REQUIEREN AUTENTICACIÓN)
# ============================================

@login_required
def index(request: HttpRequest) -> HttpResponse:
    """Vista principal que muestra el template (requiere login)"""
    return render(request, 'detector/index.html')

def gen_frames() -> Generator[bytes, None, None]:
    """Generador con MobileNet-SSD (OpenCV DNN) para máxima precisión"""
    global people_count, current_event_id, last_saved_count, camera_active, camera_instance
    
    # Inicializar cámara
    camera_instance = cv2.VideoCapture(0)
    camera_instance.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera_instance.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    camera_instance.set(cv2.CAP_PROP_FPS, 30)
    camera_active = True
    
    # Verificar si existe el modelo MobileNet-SSD
    use_mobilenet: bool = os.path.exists(PROTOTXT) and os.path.exists(CAFFEMODEL)
    
    net: Optional[Any] = None
    hog: Optional[Any] = None
    
    if use_mobilenet:
        # Cargar MobileNet-SSD con OpenCV DNN
        net = cv2.dnn.readNetFromCaffe(PROTOTXT, CAFFEMODEL)
        print("✅ Usando MobileNet-SSD con OpenCV DNN - Precisión mejorada")
    else:
        # Fallback a HOG si no hay modelo
        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        print("⚠️ MobileNet-SSD no encontrado. Ejecuta: .\\descargar_modelo.ps1")
        print("📍 Usando HOG (precisión limitada)")
    
    # Buffer para suavizado temporal
    count_buffer: List[int] = []
    frame_counter: int = 0
    
    # Tracking de personas (simplificado por posición)
    tracked_persons: Dict[int, Any] = {}
    next_person_id: int = 1
    
    while camera_active:
        success: bool
        frame: Any
        success, frame = camera_instance.read()  # type: ignore
        if not success:
            break
        
        # Efecto espejo
        frame = cv2.flip(frame, 1)
        h: int
        w: int
        h, w = frame.shape[:2]
        
        boxes: List[List[int]] = []
        confidences: List[float] = []
        
        if use_mobilenet:
            # ===== DETECCIÓN CON MOBILENET-SSD (ALTA PRECISIÓN) =====
            
            # Preparar imagen para la red neuronal
            blob: Any = cv2.dnn.blobFromImage(  # type: ignore
                cv2.resize(frame, (300, 300)),  # type: ignore
                0.007843,  # Factor de escala
                (300, 300), 
                127.5  # Sustracción de media
            )
            
            # Pasar imagen por la red
            net.setInput(blob)  # type: ignore
            detections: Any = net.forward()  # type: ignore
            
            # Procesar cada detección
            for i in range(detections.shape[2]):  # type: ignore
                confidence = float(detections[0, 0, i, 2])
                class_id = int(detections[0, 0, i, 1])
                
                # Filtrar: solo personas con confianza > 50%
                if class_id == CLASS_PERSON and confidence > 0.5:
                    # Obtener coordenadas del rectángulo
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (x1, y1, x2, y2) = box.astype("int")
                    
                    # Asegurar que las coordenadas estén dentro del frame
                    x = max(0, x1)
                    y = max(0, y1)
                    box_w = max(0, x2 - x1)
                    box_h = max(0, y2 - y1)
                    
                    # Filtro adicional: validar proporciones humanas
                    if box_h > 0 and box_w > 0:
                        aspect_ratio = box_h / box_w
                        area = box_w * box_h
                        
                        # Proporción altura/ancho típica: 1.2 a 4.0
                        # Área mínima: 1500 píxeles
                        if 1.2 <= aspect_ratio <= 4.0 and area > 1500:
                            boxes.append([x, y, box_w, box_h])
                            confidences.append(confidence)
            
            # Non-Maximum Suppression (eliminar detecciones superpuestas)
            if len(boxes) > 0:
                indices = cv2.dnn.NMSBoxes(
                    boxes, 
                    confidences, 
                    score_threshold=0.5,  # Confianza mínima
                    nms_threshold=0.3     # Umbral de IoU
                )
                
                # Mantener solo las mejores detecciones
                final_boxes = []
                if len(indices) > 0:
                    for i in indices.flatten():
                        final_boxes.append(boxes[i])
                boxes = final_boxes
            else:
                boxes = []
        
        else:
            # ===== FALLBACK: HOG DETECTOR (MENOR PRECISIÓN) =====
            rects: Any
            weights: Any
            rects, weights = hog.detectMultiScale(  # type: ignore
                frame, 
                winStride=(4, 4),
                padding=(16, 16), 
                scale=1.05
            )
            
            # Filtrar por confianza
            for i, (x, y, w, h) in enumerate(rects):
                if weights[i] > 0.5:
                    boxes.append([x, y, w, h])
        
        # Actualizar contador con suavizado temporal
        person_count: int = len(boxes)
        count_buffer.append(person_count)
        
        if len(count_buffer) > 5:
            count_buffer.pop(0)
        
        # Usar la moda (valor más frecuente) para estabilidad
        if len(count_buffer) >= 3:
            people_count = max(set(count_buffer), key=count_buffer.count)
        else:
            people_count = person_count
        
        # Guardar evento en base de datos cuando cambia el conteo
        frame_counter += 1
        if frame_counter % 30 == 0:  # Cada 30 frames (aproximadamente 1 segundo)
            if people_count != last_saved_count:
                current_event_id = f"EVT-{uuid.uuid4().hex[:8].upper()}"
                try:
                    PersonCountEvent.objects.create(
                        event_id=current_event_id,
                        person_count=people_count
                    )
                    last_saved_count = people_count
                    print(f"💾 Evento guardado: {current_event_id} - {people_count} persona(s)")
                except Exception as e:
                    print(f"Error guardando evento: {e}")
        
        # Dibujar rectángulos verdes alrededor de las personas
        for (x, y, w, h) in boxes:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)  # type: ignore
        
        # Mostrar contador en el frame
        cv2.putText(  # type: ignore
            frame, 
            f'Personas: {people_count}', 
            (10, 40),
            cv2.FONT_HERSHEY_SIMPLEX,  # type: ignore
            1.2, 
            (0, 255, 0), 
            3,
            cv2.LINE_AA  # type: ignore
        )
        
        # Codificar frame a JPEG
        _: bool
        buffer: Any
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])  # type: ignore
        frame_out: bytes = buffer.tobytes()  # type: ignore
        
        # Enviar frame al navegador
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_out + b'\r\n')
    
    # Liberar cámara al terminar
    if camera_instance:
        camera_instance.release()
        camera_instance = None

def video_feed(request: HttpRequest) -> StreamingHttpResponse:
    """Vista que devuelve el streaming de video"""
    return StreamingHttpResponse(
        gen_frames(),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )

def stop_camera(request: HttpRequest) -> JsonResponse:
    """API para detener la cámara"""
    global camera_active, camera_instance, people_count, current_event_id
    
    camera_active = False
    if camera_instance:
        camera_instance.release()
        camera_instance = None
    
    people_count = 0
    current_event_id = None
    
    return JsonResponse({'status': 'stopped'})

def get_recent_events(request: HttpRequest) -> JsonResponse:
    """API para obtener los últimos 10 eventos de detección"""
    events = PersonCountEvent.objects.all()[:10]
    data: Dict[str, Any] = {
        'events': [
            {
                'id': event.event_id,
                'count': event.person_count,
                'timestamp': event.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'time_only': event.timestamp.strftime('%H:%M:%S'),
            }
            for event in events
        ],
        'current_count': people_count,
        'current_event_id': current_event_id or 'N/A'
    }
    return JsonResponse(data)
