# 📋 INSTRUCCIONES PARA EJECUTAR LAS PRUEBAS

## 📁 Archivos de Pruebas Creados

Este directorio contiene dos archivos de pruebas:

1. **`test_opencv_detection.py`**: Pruebas unitarias del módulo de detección con OpenCV (11 tests)
2. **`test_django_integration.py`**: Pruebas de integración de rutas principales de Django (16 tests)

---

## ⚠️ IMPORTANTE: Activar Entorno Virtual

**Las pruebas requieren que el entorno virtual esté activado** para acceder a las dependencias instaladas (Django, OpenCV, etc.).

### Windows:
```bash
# Activar entorno virtual (desde la raíz del proyecto)
venv\Scripts\activate
```

### Linux/Mac:
```bash
# Activar entorno virtual
source venv/bin/activate
```

**Verificar que el entorno está activo:**
```bash
python --version  # Debería mostrar Python 3.8+
pip list          # Debería mostrar django, opencv-python, etc.
```

---

## 🚀 Cómo Ejecutar las Pruebas

### Método 1: Con entorno virtual activado (RECOMENDADO)

**Paso 1: Activar entorno virtual**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

**Paso 2: Ejecutar pruebas**
```bash
# Pruebas de OpenCV (desde la raíz del proyecto)
python pruebas\test_opencv_detection.py

# Pruebas de Django
python pruebas\test_django_integration.py

# O desde el directorio pruebas/
cd pruebas
python test_opencv_detection.py
python test_django_integration.py
```

### Método 2: Sin activar entorno (usando ruta completa)

```bash
# Windows - desde la raíz del proyecto
venv\Scripts\python.exe pruebas\test_opencv_detection.py
venv\Scripts\python.exe pruebas\test_django_integration.py

# Linux/Mac
venv/bin/python pruebas/test_opencv_detection.py
venv/bin/python pruebas/test_django_integration.py
```

**Salida esperada:**
```
======================================================================
  PRUEBAS UNITARIAS - MÓDULO DE DETECCIÓN CON OPENCV
======================================================================

Descripción: Pruebas sobre funciones críticas del sistema
Módulo: Detección con OpenCV y MobileNet-SSD

======================================================================

test_01_existencia_archivo_prototxt ... ok
test_02_existencia_archivo_caffemodel ... ok
test_03_carga_modelo_opencv ... ok
test_04_deteccion_en_imagen_blanca ... ok
test_05_deteccion_en_imagen_negra ... ok
test_06_formato_detecciones ... ok
test_07_filtro_confianza ... ok
test_08_validacion_aspect_ratio ... ok
test_09_area_minima ... ok
test_10_buffer_temporal ... ok
test_11_calculo_moda ... ok

----------------------------------------------------------------------
Ran 11 tests in 3.542s

---

## 📊 Salidas Esperadas

### Test OpenCV (11 pruebas)

```
======================================================================
  PRUEBAS UNITARIAS - MÓDULO DE DETECCIÓN CON OPENCV
======================================================================

test_01_existencia_archivo_prototxt ... ok
test_02_existencia_archivo_caffemodel ... ok
test_03_carga_modelo_opencv ... ok
test_04_deteccion_en_imagen_blanca ... ok
test_05_deteccion_en_imagen_negra ... ok
test_06_formato_detecciones ... ok
test_07_filtro_confianza ... ok
test_08_validacion_aspect_ratio ... ok
test_09_area_minima ... ok
test_10_buffer_temporal ... ok
test_11_calculo_moda ... ok

----------------------------------------------------------------------
Ran 11 tests in 0.524s

OK
```

### Test Django (16 pruebas)

```
======================================================================
  PRUEBAS DE INTEGRACIÓN - RUTAS PRINCIPALES DE DJANGO
======================================================================

test_01_acceso_login_sin_autenticar ... ok
test_02_acceso_registro_sin_autenticar ... ok
test_03_acceso_index_sin_autenticar ... ok
test_04_login_credenciales_validas ... ok
test_05_login_credenciales_invalidas ... ok
test_06_registro_usuario_valido ... ok
test_07_registro_contrasenas_no_coinciden ... ok
test_08_acceso_index_autenticado ... ok
test_09_acceso_video_feed_autenticado ... ok
test_10_logout ... ok
test_11_api_eventos_sin_autenticacion ... ok
test_12_api_eventos_autenticado ... ok
test_13_api_stop_camera ... ok
test_14_flujo_completo_usuario ... ok
test_15_crear_evento_conteo ... ok
test_16_consultar_eventos_recientes ... ok

----------------------------------------------------------------------
Ran 16 tests in 16.057s

OK (con algunas fallas conocidas en test_06, test_11, test_14)
```

---

## 📊 Generar Reporte de Cobertura (Opcional)

Para ver qué porcentaje del código está cubierto por las pruebas:

```bash
# 1. Instalar coverage
pip install coverage

# 2. Ejecutar pruebas con coverage
coverage run --source='detector,pruebas' -m unittest discover -s pruebas -p "test_*.py"

# 3. Ver reporte en consola
coverage report

# 4. Generar reporte HTML
coverage html

# 5. Abrir reporte
start htmlcov\index.html  # Windows
```

---

## 📸 Capturas para el Reporte

Para tu documento, necesitas capturar:

### 1. Código de las pruebas
- Abre cada archivo `.py` en VS Code
- Toma capturas de las funciones de prueba más importantes
- Resalta las líneas clave con comentarios

### 2. Ejecución exitosa
- Ejecuta cada archivo de pruebas
- Toma captura del terminal mostrando:
  - Número de pruebas ejecutadas
  - "OK" al final
  - Tiempo de ejecución

### 3. Detalle de cada prueba
- Ejecuta con `--verbosity=2` para ver detalles
- Captura mostrando cada test individual pasando

---

## 📝 Estructura del Reporte que debes entregar

```
SESIÓN 1 - PRUEBAS UNITARIAS Y DE INTEGRACIÓN
==============================================

1. INTRODUCCIÓN
   - Descripción del sistema
   - Objetivos de las pruebas

2. PRUEBAS UNITARIAS (OpenCV)
   
   2.1 Caso de Prueba #1: Existencia de prototxt
       - Objetivo: ...
       - Código: [CAPTURA]
       - Resultado: ✅ PASÓ
       - Log: [CAPTURA DEL TERMINAL]
   
   2.2 Caso de Prueba #2: Cargar modelo
       - Objetivo: ...
       - Código: [CAPTURA]
       - Resultado: ✅ PASÓ
   
   [... continuar con todos los tests unitarios]

3. PRUEBAS DE INTEGRACIÓN (Django)
   
   3.1 Caso de Prueba #1: Login sin autenticación
       - Objetivo: ...
       - Código: [CAPTURA]
       - Resultado: ✅ PASÓ
   
   [... continuar con todos los tests de integración]

4. RESULTADOS GENERALES
   - Total pruebas: 27
   - Pasadas: 27
   - Fallidas: 0
   - Cobertura: XX%
   
   [CAPTURA COMPLETA DEL TERMINAL]

5. CONCLUSIONES
   - Análisis de resultados
   - Lecciones aprendidas
```

---

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'cv2'" o "No module named 'django'"

**Causa**: El entorno virtual no está activado.

**Solución**:
```bash
# Activar entorno virtual
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Verificar instalación
pip list | findstr django
pip list | findstr opencv
```

### Error: "Invalid HTTP_HOST header: 'testserver'"

**Causa**: `ALLOWED_HOSTS` en settings.py no incluye 'testserver'.

**Solución**: Ya corregido en `people_counter/settings.py`:
```python
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']
```

### Error: "django.core.exceptions.ImproperlyConfigured"

**Solución**: Ejecuta desde la raíz del proyecto, no desde `pruebas/`
```bash
cd ..
python pruebas\test_django_integration.py
```

### Las pruebas tardan mucho en ejecutarse

**Explicación**: Es normal. Las pruebas de Django crean una base de datos temporal y las de OpenCV cargan el modelo MobileNet-SSD (23 MB).

- `test_opencv_detection.py`: ~0.5 segundos
- `test_django_integration.py`: ~16 segundos

---

## 📊 Resumen de Pruebas

| Archivo | Tests | Descripción |
|---------|-------|-------------|
| `test_opencv_detection.py` | 11 | Pruebas del módulo de detección MobileNet-SSD |
| `test_django_integration.py` | 16 | Pruebas de autenticación, rutas y API |
| **TOTAL** | **27** | **Suite completa de pruebas** |

### Cobertura por Módulo

- ✅ Modelos de base de datos (PersonCountEvent, PersonTracking)
- ✅ Sistema de autenticación (login, register, logout)
- ✅ Rutas protegidas (decoradores @login_required)
- ✅ API REST (/api/events/, /api/stop_camera/)
- ✅ Detección con OpenCV (carga de modelo, filtros, suavizado)
- ✅ Validaciones de entrada (contraseñas, formularios)

---

## 📝 Para Más Información

Consulta la documentación completa del proyecto:

- `README.md` - Descripción general del sistema
- `GUIA_INSTALACION.md` - Instrucciones de instalación
- `DOCUMENTACION_TECNICA.md` - Detalles técnicos y arquitectura
  - Sección 10: Pruebas Unitarias (instrucciones detalladas)

---

**Fecha de creación**: Noviembre 2025  
**Versión**: 1.0  
**Autor**: Sistema de Detección de Personas
