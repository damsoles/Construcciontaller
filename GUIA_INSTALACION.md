# 📦 Guía de Instalación - Sistema de Detección de Personas

Sistema completo de detección y tracking de personas con OpenCV, MobileNet-SSD y Django.

---

## 📋 Requisitos Previos

### 1. Software Necesario

- **Python 3.8 o superior** (Recomendado: Python 3.10+)
  - Descargar desde: https://www.python.org/downloads/
  - ⚠️ Durante la instalación, marcar **"Add Python to PATH"**

- **Git** (para clonar el repositorio)
  - Descargar desde: https://git-scm.com/downloads

- **Cámara web funcional** (integrada o USB)

### 2. Espacio en Disco

- Mínimo: **500 MB**
- Recomendado: **1 GB** (incluye dependencias y modelo)

---

## 🚀 Instalación Paso a Paso

### **PASO 1: Clonar el Repositorio**

Abre tu terminal (CMD, PowerShell o Terminal) y ejecuta:

```bash
git clone https://github.com/damsoles/Construcciontaller.git
cd Construcciontaller/contador_personas_lab
```

O descarga el ZIP desde GitHub y descomprímelo.

---

### **PASO 2: Crear el Entorno Virtual**

El entorno virtual aísla las dependencias del proyecto.

**En Windows (PowerShell/CMD):**
```bash
python -m venv venv
```

**En Mac/Linux:**
```bash
python3 -m venv venv
```

---

### **PASO 3: Activar el Entorno Virtual**

**En Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

**En Windows (CMD):**
```bash
venv\Scripts\activate.bat
```

**En Mac/Linux:**
```bash
source venv/bin/activate
```

✅ Deberías ver `(venv)` al inicio de tu línea de comandos.

---

### **PASO 4: Instalar Dependencias de Python**

Con el entorno virtual activo, instala todas las dependencias:

```bash
pip install -r requirements.txt
```

**Dependencias que se instalarán:**

| Paquete | Versión | Descripción |
|---------|---------|-------------|
| Django | 5.2 | Framework web |
| opencv-contrib-python | 4.6.0.66 | Visión por computadora con módulo DNN |
| numpy | 1.26.4 | Operaciones numéricas |
| imutils | 0.5.4 | Utilidades de imagen |
| asgiref | 3.8.1 | Soporte ASGI para Django |
| sqlparse | 0.5.3 | Parser SQL para Django |
| tzdata | 2025.2 | Datos de zonas horarias |

⏱️ **Tiempo estimado:** 2-5 minutos dependiendo de tu conexión.

---

### **PASO 5: Descargar el Modelo MobileNet-SSD**

Este modelo pre-entrenado es esencial para la detección de alta precisión (85-95%).

**En Windows (PowerShell):**
```bash
.\descargar_modelo.ps1
```

**En Mac/Linux:**
```bash
# Crear directorio
mkdir -p detector/models

# Descargar prototxt (configuración del modelo)
curl -o detector/models/MobileNetSSD_deploy.prototxt \
  https://github.com/PINTO0309/MobileNet-SSD-RealSense/raw/master/caffemodel/MobileNetSSD/MobileNetSSD_deploy.prototxt

# Descargar caffemodel (pesos del modelo - 23 MB)
curl -L -o detector/models/MobileNetSSD_deploy.caffemodel \
  https://github.com/PINTO0309/MobileNet-SSD-RealSense/raw/master/caffemodel/MobileNetSSD/MobileNetSSD_deploy.caffemodel
```

✅ **Archivos descargados:**
- `detector/models/MobileNetSSD_deploy.prototxt` (~30 KB)
- `detector/models/MobileNetSSD_deploy.caffemodel` (~23 MB)

⏱️ **Tiempo estimado:** 30-60 segundos

---

### **PASO 6: Aplicar Migraciones de Base de Datos**

Django necesita crear las tablas en SQLite:

```bash
python manage.py migrate
```

✅ **Tablas creadas:**
- `detector_personcountev` - Eventos de detección
- `detector_persontracking` - Tracking de personas
- Tablas del sistema Django (auth, admin, sessions, etc.)

---

### **PASO 7: (Opcional) Crear Superusuario**

Para acceder al panel de administración de Django:

```bash
python manage.py createsuperuser
```

Se te pedirá:
- **Username:** Tu nombre de usuario
- **Email:** Tu correo (opcional, puedes dejarlo vacío)
- **Password:** Tu contraseña (no se verá mientras escribes)

---

### **PASO 8: Iniciar el Servidor**

```bash
python manage.py runserver
```

✅ **Mensaje esperado:**
```
Starting development server at http://127.0.0.1:8000/
✅ Usando MobileNet-SSD con OpenCV DNN - Precisión mejorada
```

---

## 🌐 Acceso al Sistema

Una vez que el servidor esté corriendo:

### **Aplicación Principal**
```
http://127.0.0.1:8000/
```
- Video en tiempo real de la cámara
- Detección de personas con MobileNet-SSD
- Historial de eventos con IDs únicos
- Actualización automática cada 2 segundos

### **API REST (JSON)**
```
http://127.0.0.1:8000/api/events/
```
Respuesta:
```json
{
  "events": [
    {
      "id": "EVT-A1B2C3D4",
      "count": 2,
      "timestamp": "2025-10-27 16:30:45",
      "time_only": "16:30:45"
    }
  ],
  "current_count": 2,
  "current_event_id": "EVT-A1B2C3D4"
}
```

### **Panel de Administración**
```
http://127.0.0.1:8000/admin/
```
- Requiere superusuario (PASO 7)
- Ver todos los eventos almacenados
- Administrar base de datos

---

## ✅ Verificación de Instalación

### **Checklist Completo**

- [ ] Python 3.8+ instalado
- [ ] Repositorio clonado
- [ ] Entorno virtual creado y activado `(venv)`
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Modelo MobileNet-SSD descargado (23 MB)
- [ ] Migraciones aplicadas (`python manage.py migrate`)
- [ ] Servidor corriendo sin errores
- [ ] Navegador abierto en http://127.0.0.1:8000/
- [ ] Cámara funcionando (permitir acceso cuando lo pida)
- [ ] Detección de personas operativa

---

## 🛠️ Solución de Problemas

### ❌ **Error: "python no se reconoce como comando"**

**Solución:**
- Verifica que Python esté en el PATH del sistema
- Reinstala Python marcando "Add Python to PATH"
- En Windows, usa `py` en lugar de `python`

### ❌ **Error: "No module named 'cv2'"**

**Solución:**
```bash
pip install opencv-contrib-python==4.6.0.66
```

### ❌ **Error: "No se encuentra la cámara"**

**Solución:**
- Verifica que la cámara esté conectada
- Cierra otras aplicaciones que usen la cámara (Zoom, Teams, etc.)
- En Windows, ve a Configuración > Privacidad > Cámara y permite el acceso

### ❌ **Error: "Port 8000 is already in use"**

**Solución:**
```bash
# Usar otro puerto
python manage.py runserver 8080

# O detener el proceso que usa el puerto 8000
```

### ❌ **El modelo no se descargó correctamente**

**Solución:**
1. Descarga manualmente los archivos desde:
   - Prototxt: https://github.com/PINTO0309/MobileNet-SSD-RealSense/raw/master/caffemodel/MobileNetSSD/MobileNetSSD_deploy.prototxt
   - Caffemodel: https://github.com/PINTO0309/MobileNet-SSD-RealSense/raw/master/caffemodel/MobileNetSSD/MobileNetSSD_deploy.caffemodel

2. Guárdalos en: `detector/models/`

**Nota:** El sistema funcionará con HOG como respaldo si no encuentra el modelo, pero con menor precisión (60-70% vs 85-95%).

### ❌ **Error de migraciones**

**Solución:**
```bash
# Eliminar base de datos y recrear
rm db.sqlite3
python manage.py migrate
```

---

## 🔄 Actualizar el Sistema

Si hay actualizaciones en el repositorio:

```bash
# Detener el servidor (Ctrl+C)

# Actualizar código
git pull origin main

# Activar entorno virtual
venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate    # Mac/Linux

# Actualizar dependencias
pip install -r requirements.txt --upgrade

# Aplicar nuevas migraciones
python manage.py migrate

# Reiniciar servidor
python manage.py runserver
```

---

## 📊 Estructura del Proyecto

```
contador_personas_lab/
├── detector/
│   ├── migrations/         # Migraciones de base de datos
│   ├── models/             # Modelos MobileNet-SSD
│   │   ├── MobileNetSSD_deploy.prototxt
│   │   └── MobileNetSSD_deploy.caffemodel
│   ├── templates/detector/ # Templates HTML
│   │   └── index.html
│   ├── admin.py           # Configuración del admin
│   ├── models.py          # Modelos de datos
│   ├── urls.py            # URLs de la app
│   └── views.py           # Lógica de negocio
├── people_counter/        # Configuración Django
│   ├── settings.py
│   └── urls.py
├── db.sqlite3             # Base de datos SQLite
├── manage.py              # Script de gestión Django
├── requirements.txt       # Dependencias Python
├── descargar_modelo.ps1   # Script para descargar modelo
├── README.md              # Documentación general
├── GUIA_INSTALACION.md    # Esta guía
└── venv/                  # Entorno virtual (ignorado en Git)
```

---

## 💻 Comandos Útiles

```bash
# Activar entorno virtual
venv\Scripts\Activate.ps1         # Windows PowerShell
venv\Scripts\activate.bat         # Windows CMD
source venv/bin/activate          # Mac/Linux

# Instalar dependencias
pip install -r requirements.txt

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver

# Iniciar en otro puerto
python manage.py runserver 8080

# Ver modelos registrados
python manage.py showmigrations

# Shell de Django (para pruebas)
python manage.py shell

# Colectar archivos estáticos (producción)
python manage.py collectstatic
```

---

## 📚 Recursos Adicionales

- **Repositorio GitHub:** https://github.com/damsoles/Construcciontaller
- **Documentación Django:** https://docs.djangoproject.com/
- **Documentación OpenCV:** https://docs.opencv.org/
- **OpenCV DNN Module:** https://docs.opencv.org/master/d2/d58/tutorial_table_of_content_dnn.html
- **MobileNet Paper:** https://arxiv.org/abs/1704.04861

---

## 🎓 Conceptos Clave

### **MobileNet-SSD**
- Red neuronal optimizada para CPU
- 85-95% de precisión en detección de personas
- 30+ FPS en tiempo real
- Modelo pre-entrenado en COCO dataset

### **OpenCV DNN**
- Módulo de Deep Learning integrado en OpenCV
- No requiere TensorFlow/PyTorch
- Compatible con Caffe, TensorFlow, PyTorch, ONNX

### **SQLite**
- Base de datos integrada, sin servidor
- Almacena eventos de detección
- Ubicación: `db.sqlite3`

---

## 👨‍💻 Soporte

Si tienes problemas durante la instalación:

1. **Revisa esta guía** completa
2. **Verifica los requisitos** del sistema
3. **Consulta la sección de solución de problemas**
4. **Revisa el README.md** para más detalles técnicos
5. **Contacta al equipo** de desarrollo

---

## 📝 Notas Importantes

- ⚠️ Este es un **servidor de desarrollo**. Para producción, usa Gunicorn/uWSGI + Nginx
- ⚠️ La base de datos SQLite **no se sincroniza con Git** (.gitignore)
- ⚠️ El entorno virtual `venv/` **no se sube a Git** (.gitignore)
- ⚠️ Mantén actualizado el sistema: `git pull` regularmente
- ✅ Los eventos se guardan automáticamente cada vez que cambia el número de personas

---

## ✨ ¡Listo para Usar!

Una vez completados todos los pasos, tendrás:

✅ Sistema de detección funcionando  
✅ Base de datos SQLite operativa  
✅ Interfaz web profesional  
✅ API REST disponible  
✅ Historial de eventos en tiempo real  
✅ Precisión de 85-95% con MobileNet-SSD  

**¡Disfruta del sistema! 🚀**
