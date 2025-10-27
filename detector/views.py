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
    """Generador que procesa frames de video"""
    global people_count
    
    # Inicializar captura de video (0 = cámara predeterminada)
    camera = cv2.VideoCapture(0)
    
    # Inicializar detector HOG para personas
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    
    while True:
        # Leer frame de la cámara
        success, frame = camera.read()
        
        if not success:
            break
        
        # Redimensionar para mejorar rendimiento
        frame = cv2.resize(frame, (640, 480))
        
        # Detectar personas en el frame
        boxes, weights = hog.detectMultiScale(
            frame, 
            winStride=(8, 8),
            padding=(4, 4), 
            scale=1.05
        )
        
        # Actualizar contador
        people_count = len(boxes)
        
        # Dibujar rectángulos alrededor de las personas detectadas
        for (x, y, w, h) in boxes:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Mostrar contador en el frame
        cv2.putText(
            frame, 
            f'Personas: {people_count}', 
            (10, 40),
            cv2.FONT_HERSHEY_SIMPLEX, 
            1.2, 
            (0, 0, 255), 
            3
        )
        
        # Codificar frame a formato JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
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
