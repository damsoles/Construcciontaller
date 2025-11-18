# 📘 Documentación Técnica - Sistema de Detección de Personas

## 1. Requisitos del Sistema

### Hardware Mínimo
- **Procesador**: Intel Core i3 o equivalente
- **RAM**: 4 GB mínimo (8 GB recomendado)
- **Cámara Web**: Resolución mínima 640x480
- **Almacenamiento**: 500 MB libres

### Software
- **Sistema Operativo**: Windows 10/11, macOS 10.14+, Ubuntu 20.04+
- **Python**: 3.8 o superior
- **Navegador**: Chrome 90+, Firefox 88+, Edge 90+

---

## 2. Arquitectura del Sistema

### 2.1 Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────┐
│                    NAVEGADOR WEB                         │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐ │
│  │   Login/    │  │   Video      │  │   Historial    │ │
│  │  Register   │  │   Stream     │  │   Eventos      │ │
│  └──────┬──────┘  └──────┬───────┘  └────────┬───────┘ │
└─────────┼─────────────────┼───────────────────┼─────────┘
          │                 │                   │
          ▼                 ▼                   ▼
┌─────────────────────────────────────────────────────────┐
│                    DJANGO SERVER                         │
│  ┌──────────────┐  ┌─────────────┐  ┌────────────────┐ │
│  │ Autenticación│  │   Views     │  │   API REST     │ │
│  │  (auth)      │  │  (video)    │  │  (eventos)     │ │
│  └──────┬───────┘  └──────┬──────┘  └────────┬───────┘ │
│         │                 │                   │          │
│         ▼                 ▼                   ▼          │
│  ┌──────────────────────────────────────────────────┐  │
│  │            DETECTOR (views.py)                    │  │
│  │  ┌───────────────┐    ┌──────────────────────┐  │  │
│  │  │   MobileNet   │    │   Tracking System    │  │  │
│  │  │   SSD + DNN   │───▶│   (UUID + Buffer)    │  │  │
│  │  └───────┬───────┘    └──────────┬───────────┘  │  │
│  └──────────┼──────────────────────┼────────────────┘  │
└─────────────┼──────────────────────┼─────────────────┘
              ▼                      ▼
┌──────────────────────┐  ┌────────────────────────┐
│   OpenCV Camera      │  │   SQLite Database      │
│   cv2.VideoCapture   │  │   - PersonCountEvent   │
└──────────────────────┘  │   - PersonTracking     │
                          └────────────────────────┘
```

### 2.2 Flujo de Datos

1. **Captura**: `cv2.VideoCapture(0)` obtiene frames de la cámara
2. **Preprocesamiento**: `cv2.dnn.blobFromImage()` normaliza la imagen a 300x300
3. **Detección**: MobileNet-SSD identifica personas en el frame
4. **Filtrado**: Confianza > 50%, aspect ratio 1.2-4.0, área > 2000px
5. **NMS**: `cv2.dnn.NMSBoxes()` elimina detecciones duplicadas
6. **Tracking**: Buffer de 5 frames con moda estadística para estabilidad
7. **Almacenamiento**: Guarda en SQLite cuando cambia el conteo
8. **Streaming**: MJPEG sobre HTTP a través de `StreamingHttpResponse`

---

## 3. Estructura de Directorios

```
contador_personas_lab/
│
├── detector/                      # Aplicación principal
│   ├── models.py                  # Modelos de BD
│   ├── views.py                   # Lógica de detección y autenticación
│   ├── urls.py                    # Rutas de la app
│   ├── admin.py                   # Configuración del admin
│   ├── tests.py                   # Pruebas unitarias
│   │
│   ├── templates/detector/
│   │   ├── login.html             # Página de login
│   │   ├── register.html          # Página de registro
│   │   └── index.html             # Dashboard principal
│   │
│   ├── models/                    # Modelos pre-entrenados
│   │   ├── MobileNetSSD_deploy.prototxt
│   │   └── MobileNetSSD_deploy.caffemodel (23MB)
│   │
│   └── media/                     # Recursos estáticos
│       ├── logo conteo.png
│       └── imagen fondo.png
│
├── people_counter/                # Configuración del proyecto
│   ├── settings.py                # Configuración global
│   ├── urls.py                    # Rutas principales
│   └── wsgi.py                    # Punto de entrada WSGI
│
├── venv/                          # Entorno virtual (no en git)
├── db.sqlite3                     # Base de datos SQLite
├── manage.py                      # CLI de Django
├── requirements.txt               # Dependencias del proyecto
├── README.md                      # Documentación principal
└── GUIA_INSTALACION.md           # Guía de instalación
```

---

## 4. Modelos de Base de Datos

### 4.1 PersonCountEvent

```python
class PersonCountEvent(models.Model):
    event_id = CharField(max_length=20, unique=True)  # EVT-XXXXXXXX
    person_count = PositiveIntegerField(default=0)
    timestamp = DateTimeField(auto_now_add=True)
```

**Propósito**: Registrar cada cambio en el número de personas detectadas.

**Campos**:
- `event_id`: Identificador único generado con UUID (8 caracteres hexadecimales)
- `person_count`: Número de personas detectadas en ese momento
- `timestamp`: Fecha y hora exacta de la detección

**Ejemplo**:
```python
evento = PersonCountEvent.objects.create(
    event_id='EVT-A1B2C3D4',
    person_count=3
)
```

### 4.2 PersonTracking

```python
class PersonTracking(models.Model):
    person_id = PositiveIntegerField(unique=True)
    first_seen = DateTimeField(auto_now_add=True)
    last_seen = DateTimeField(auto_now=True)
    detection_count = PositiveIntegerField(default=1)
```

**Propósito**: Tracking individual de personas a lo largo del tiempo.

**Campos**:
- `person_id`: ID único de la persona detectada
- `first_seen`: Primera vez que fue detectada
- `last_seen`: Última vez vista (actualizado automáticamente)
- `detection_count`: Número total de veces detectada

---

## 5. APIs Disponibles

### 5.1 GET /api/events/

**Descripción**: Obtiene los últimos 10 eventos de detección.

**Autenticación**: Requerida (`@login_required`)

**Método**: GET

**Respuesta exitosa (200)**:
```json
{
  "events": [
    {
      "id": "EVT-A1B2C3D4",
      "count": 2,
      "timestamp": "2025-11-17 20:30:45",
      "time_only": "20:30:45"
    },
    {
      "id": "EVT-B5C6D7E8",
      "count": 1,
      "timestamp": "2025-11-17 20:29:30",
      "time_only": "20:29:30"
    }
  ],
  "current_count": 2,
  "current_event_id": "EVT-A1B2C3D4"
}
```

**Uso en JavaScript**:
```javascript
fetch('/api/events/')
  .then(response => response.json())
  .then(data => {
    console.log('Personas actuales:', data.current_count);
    console.log('Eventos:', data.events);
  });
```

### 5.2 POST /api/stop_camera/

**Descripción**: Detiene la cámara y libera recursos del sistema.

**Autenticación**: Requerida

**Método**: POST

**Respuesta exitosa (200)**:
```json
{
  "status": "stopped"
}
```

**Uso en JavaScript**:
```javascript
fetch('/api/stop_camera/', {
  method: 'POST',
  headers: {
    'X-CSRFToken': getCookie('csrftoken')
  }
})
.then(response => response.json())
.then(data => console.log('Cámara detenida:', data.status));
```

---

## 6. Algoritmo de Detección

### 6.1 MobileNet-SSD

**Características**:
- **Arquitectura**: MobileNet v1 con SSD (Single Shot Detector)
- **Input**: 300x300x3 (RGB normalizado)
- **Output**: 20 clases de objetos del dataset COCO
- **Clase persona**: Índice 15
- **Precisión**: 85-95% en detección de personas
- **FPS**: 30+ en CPU moderna

**Parámetros de detección**:
```python
confidence_threshold = 0.5      # 50% confianza mínima
aspect_ratio_range = (1.2, 4.0) # Proporciones humanas típicas
min_area = 2000                 # Píxeles mínimos del bounding box
nms_threshold = 0.3             # IoU para Non-Maximum Suppression
```

**Proceso de detección**:
```python
# 1. Preprocesar imagen
blob = cv2.dnn.blobFromImage(
    cv2.resize(frame, (300, 300)),
    0.007843,      # Factor de escala
    (300, 300),    # Tamaño de entrada
    127.5          # Mean subtraction
)

# 2. Forward pass
net.setInput(blob)
detections = net.forward()

# 3. Procesar detecciones
for i in range(detections.shape[2]):
    confidence = detections[0, 0, i, 2]
    class_id = int(detections[0, 0, i, 1])
    
    if class_id == 15 and confidence > 0.5:
        # Persona detectada con confianza suficiente
        box = detections[0, 0, i, 3:7]
        # Procesar bounding box...
```

### 6.2 Suavizado Temporal

```python
count_buffer = []  # Buffer circular de últimos 5 frames

# Agregar nueva detección
count_buffer.append(person_count)
if len(count_buffer) > 5:
    count_buffer.pop(0)

# Calcular moda (valor más frecuente)
from collections import Counter
people_count = Counter(count_buffer).most_common(1)[0][0]
```

**Propósito**: Evitar fluctuaciones rápidas en el contador causadas por:
- Detecciones temporales erróneas
- Personas entrando/saliendo del frame brevemente
- Oclusiones momentáneas

---

## 7. Sistema de Autenticación

### 7.1 Flujo de Registro

```python
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Validaciones
        if password1 != password2:
            return render(request, 'register.html', {
                'error': 'Las contraseñas no coinciden'
            })
        
        if len(password1) < 8:
            return render(request, 'register.html', {
                'error': 'La contraseña debe tener al menos 8 caracteres'
            })
        
        # Crear usuario
        user = User.objects.create_user(
            username=username,
            password=password1
        )
        login(request, user)
        return redirect('index')
```

### 7.2 Protección de Rutas

```python
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    """Vista principal - requiere autenticación"""
    return render(request, 'detector/index.html')
```

**Configuración en settings.py**:
```python
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'login'
```

---

## 8. Configuración Avanzada

### 8.1 Cambiar resolución de cámara

En `detector/views.py`, función `gen_frames()`:
```python
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)   # Ancho
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)   # Alto
camera.set(cv2.CAP_PROP_FPS, 30)             # FPS
```

**Impacto en rendimiento**:
- 640x480: ~35 FPS, uso CPU 30%
- 1280x720: ~25 FPS, uso CPU 50%
- 1920x1080: ~15 FPS, uso CPU 80%

### 8.2 Ajustar sensibilidad de detección

**Más estricto (menos falsos positivos)**:
```python
confidence_threshold = 0.7
min_area = 3000
```

**Más permisivo (más detecciones)**:
```python
confidence_threshold = 0.3
min_area = 1500
```

### 8.3 Cambiar puerto del servidor

```bash
# Puerto personalizado
python manage.py runserver 0.0.0.0:8080

# Solo local
python manage.py runserver 127.0.0.1:8000

# Acceso desde red local
python manage.py runserver 0.0.0.0:8000
```

### 8.4 Modo debug

En `people_counter/settings.py`:
```python
# Desarrollo
DEBUG = True
ALLOWED_HOSTS = []

# Producción
DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'tudominio.com']
```

---

## 9. Solución de Problemas Técnicos

### Error: "Camera not found (cv2.VideoCapture failed)"

**Causas posibles**:
1. Cámara en uso por otra aplicación
2. Drivers de cámara desactualizados
3. Permisos de sistema denegados

**Solución**:
```python
# Probar diferentes índices de cámara
for i in range(5):
    camera = cv2.VideoCapture(i)
    if camera.isOpened():
        print(f"Cámara encontrada en índice {i}")
        break
    camera.release()
```

### Error: "Model not found"

**Verificación**:
```bash
ls detector/models/
# Debe mostrar:
# MobileNetSSD_deploy.prototxt (30 KB)
# MobileNetSSD_deploy.caffemodel (23 MB)
```

**Solución**: Descargar modelo desde el repositorio

### Error: "Port 8000 is already in use"

**Solución**:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9

# O usar otro puerto
python manage.py runserver 8080
```

### Baja precisión de detección

**Checklist**:
- ✅ Iluminación adecuada (evitar contraluz)
- ✅ Distancia óptima: 1-5 metros de la cámara
- ✅ Personas de pie (no sentadas ni acostadas)
- ✅ Sin objetos grandes obstruyendo
- ✅ `confidence_threshold` configurado correctamente

**Ajuste**:
```python
# Reducir umbral si no detecta
if confidence > 0.4:  # En lugar de 0.5
    # Procesar detección
```

### Alto uso de CPU

**Optimizaciones**:
```python
# 1. Reducir resolución
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

# 2. Skip frames
frame_skip = 2
frame_count = 0

if frame_count % frame_skip == 0:
    # Procesar detección
frame_count += 1

# 3. Reducir calidad JPEG
ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
```

---

## 10. Pruebas Unitarias

### 10.1 Ejecutar pruebas

```bash
# Todas las pruebas
python manage.py test detector

# Prueba específica
python manage.py test detector.OpenCVDetectionTests.test_carga_modelo_opencv

# Con verbosidad
python manage.py test detector --verbosity=2
```

### 10.2 Cobertura de código

```bash
# Instalar coverage
pip install coverage

# Ejecutar con cobertura
coverage run --source='detector' manage.py test detector

# Ver reporte en consola
coverage report

# Generar reporte HTML
coverage html

# Abrir reporte
start htmlcov/index.html  # Windows
open htmlcov/index.html   # Mac
xdg-open htmlcov/index.html  # Linux
```

### 10.3 Pruebas de integración

```python
from django.test import Client

def test_flujo_completo():
    client = Client()
    
    # 1. Registro
    response = client.post('/register/', {
        'username': 'testuser',
        'password1': 'testpass123',
        'password2': 'testpass123'
    })
    assert response.status_code == 302
    
    # 2. Login
    response = client.post('/login/', {
        'username': 'testuser',
        'password': 'testpass123'
    })
    assert response.status_code == 302
    
    # 3. Acceso a index
    response = client.get('/')
    assert response.status_code == 200
    
    # 4. API eventos
    response = client.get('/api/events/')
    assert response.status_code == 200
    data = response.json()
    assert 'events' in data
```

---

## 11. Mantenimiento

### 11.1 Backup de Base de Datos

```bash
# Exportar todos los datos
python manage.py dumpdata > backup_completo.json

# Exportar solo app detector
python manage.py dumpdata detector > backup_detector.json

# Restaurar datos
python manage.py loaddata backup_detector.json
```

### 11.2 Limpieza de Eventos Antiguos

```python
# Shell de Django
python manage.py shell

# Eliminar eventos de hace más de 30 días
from detector.models import PersonCountEvent
from datetime import datetime, timedelta

fecha_limite = datetime.now() - timedelta(days=30)
eliminados = PersonCountEvent.objects.filter(
    timestamp__lt=fecha_limite
).delete()

print(f"Eventos eliminados: {eliminados[0]}")
```

### 11.3 Optimización de Base de Datos

```bash
# Vacuuming (SQLite)
python manage.py dbshell
> VACUUM;
> .exit

# Reindexación
> REINDEX;
```

---

## 12. Despliegue en Producción

### 12.1 Configuración

**settings.py**:
```python
DEBUG = False
ALLOWED_HOSTS = ['tu-dominio.com', 'www.tu-dominio.com']

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'detector_db',
        'USER': 'postgres',
        'PASSWORD': 'tu_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 12.2 Servidor Web (Nginx + Gunicorn)

**Instalar Gunicorn**:
```bash
pip install gunicorn
```

**Ejecutar**:
```bash
gunicorn people_counter.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

**Configuración Nginx**:
```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /path/to/staticfiles/;
    }
}
```

### 12.3 Supervisor (Auto-restart)

```ini
[program:detector]
command=/path/to/venv/bin/gunicorn people_counter.wsgi:application
directory=/path/to/contador_personas_lab
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/detector.log
```

---

## 13. Monitoreo y Logs

### 13.1 Configuración de Logs

**settings.py**:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'detector.log',
        },
    },
    'loggers': {
        'detector': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### 13.2 Métricas de Rendimiento

```python
import time
import logging

logger = logging.getLogger('detector')

def gen_frames():
    frame_times = []
    
    while camera_active:
        start_time = time.time()
        
        # Procesamiento...
        
        processing_time = time.time() - start_time
        fps = 1 / processing_time
        
        logger.info(f"FPS: {fps:.2f}, Processing: {processing_time*1000:.2f}ms")
```

---

## 14. Seguridad

### 14.1 Variables de Entorno

**.env**:
```bash
SECRET_KEY=tu-secret-key-super-segura
DEBUG=False
DATABASE_URL=postgresql://user:pass@localhost/dbname
```

**settings.py**:
```python
import os
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
```

### 14.2 Rate Limiting

```python
from django.views.decorators.cache import cache_page

@cache_page(60)  # Cache por 1 minuto
def get_recent_events(request):
    # ...
```

---

## 15. Contacto y Soporte

**Repositorio**: https://github.com/damsoles/Construcciontaller  
**Documentación**: README.md y GUIA_INSTALACION.md  
**Issues**: GitHub Issues del repositorio

---

**Versión**: 1.0  
**Fecha**: Noviembre 2025  
**Autor**: Sistema de Detección de Personas
