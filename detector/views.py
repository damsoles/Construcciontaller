import cv2
import numpy as np
from django.http import StreamingHttpResponse
from django.shortcuts import render

# Variable global para contador
people_count = 0

def index(request):
    """Vista principal que muestra el template"""
    return render(request, 'detector/index.html')

def gen_frames():
    """Generador que procesa frames de video con detección mejorada"""
    global people_count
    
    # Inicializar captura de video (0 = cámara predeterminada)
    camera = cv2.VideoCapture(0)
    
    # Configurar parámetros de la cámara para mejor calidad
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    camera.set(cv2.CAP_PROP_FPS, 30)
    
    # Inicializar detector HOG para personas
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    
    # Variables para suavizado de detección
    frame_skip = 0
    detection_threshold = 0.4  # Umbral de confianza para filtrar falsos positivos
    
    while True:
        # Leer frame de la cámara
        success, frame = camera.read()
        
        if not success:
            break
        
        # Voltear horizontalmente para efecto espejo (más natural)
        frame = cv2.flip(frame, 1)
        
        # Procesar cada 2 frames para mejor rendimiento
        frame_skip += 1
        if frame_skip % 2 == 0:
            # Detectar personas con parámetros optimizados
            boxes, weights = hog.detectMultiScale(
                frame, 
                winStride=(4, 4),      # Ventana más pequeña = mejor detección
                padding=(8, 8),        # Más padding = mejor captura de bordes
                scale=1.05,            # Escala de búsqueda
                hitThreshold=0         # Umbral de detección (0 = predeterminado)
            )
            
            # Filtrar detecciones por confianza
            if len(weights) > 0:
                # Filtrar por peso/confianza
                filtered_detections = []
                for (x, y, w, h), weight in zip(boxes, weights):
                    if weight > detection_threshold:
                        filtered_detections.append((x, y, w, h))
                
                # Actualizar contador con detecciones filtradas
                people_count = len(filtered_detections)
                
                # Dibujar rectángulos alrededor de las personas detectadas
                for (x, y, w, h) in filtered_detections:
                    # Rectángulo principal (verde)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    
                    # Etiqueta con confianza
                    label = f"Persona"
                    cv2.putText(
                        frame, 
                        label, 
                        (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        0.6, 
                        (0, 255, 0), 
                        2
                    )
            else:
                people_count = 0
        
        # Crear overlay oscuro semi-transparente para el texto
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (300, 60), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
        
        # Mostrar contador en el frame con mejor visualización
        cv2.putText(
            frame, 
            f'Personas: {people_count}', 
            (10, 40),
            cv2.FONT_HERSHEY_DUPLEX, 
            1.2, 
            (255, 255, 255), 
            2,
            cv2.LINE_AA
        )
        
        # Codificar frame a formato JPEG con calidad mejorada
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 85]
        ret, buffer = cv2.imencode('.jpg', frame, encode_param)
        frame = buffer.tobytes()
        
        # Retornar frame en formato streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    # Liberar cámara al terminar
    camera.release()

def video_feed(request):
    """Vista que sirve el streaming de video"""
    return StreamingHttpResponse(
        gen_frames(),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )
