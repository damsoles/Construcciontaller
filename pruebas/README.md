# 📋 INSTRUCCIONES PARA EJECUTAR LAS PRUEBAS

## 📁 Archivos de Pruebas Creados

Este directorio contiene dos archivos de pruebas:

1. **`test_opencv_detection.py`**: Pruebas unitarias del módulo de detección con OpenCV
2. **`test_django_integration.py`**: Pruebas de integración de rutas principales de Django

---

## 🚀 Cómo Ejecutar las Pruebas

### Opción 1: Ejecutar pruebas unitarias de OpenCV

```bash
# Desde la raíz del proyecto (contador_personas_lab/)
cd pruebas
python test_opencv_detection.py
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

OK
```

---

### Opción 2: Ejecutar pruebas de integración de Django

```bash
# Desde la raíz del proyecto
cd pruebas
python test_django_integration.py
```

**Salida esperada:**
```
======================================================================
  PRUEBAS DE INTEGRACIÓN - RUTAS PRINCIPALES DE DJANGO
======================================================================

Descripción: Validación del flujo completo de la aplicación
Módulo: Django (autenticación, rutas, API, modelos)

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
Ran 16 tests in 5.234s

OK
```

---

### Opción 3: Ejecutar todas las pruebas con Django test runner

```bash
# Desde la raíz del proyecto (NO desde pruebas/)
python manage.py test pruebas --verbosity=2
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

## ⚠️ Problemas Comunes

### Error: "ModuleNotFoundError: No module named 'django'"

**Solución**: Asegúrate de estar en el entorno virtual
```bash
cd ..  # Volver a raíz del proyecto
venv\Scripts\Activate.ps1
cd pruebas
python test_django_integration.py
```

### Error: "django.core.exceptions.ImproperlyConfigured"

**Solución**: Ejecuta desde la raíz del proyecto, no desde `pruebas/`
```bash
cd ..
python -m unittest pruebas.test_django_integration
```

### Error: "Camera not found"

**Solución**: Normal, es esperado. Las pruebas unitarias no requieren cámara física.

---

## 💡 Tips para el Reporte

1. **Capturas claras**: Usa zoom adecuado, código legible
2. **Explicación**: Cada caso de prueba debe tener:
   - Objetivo
   - Entrada
   - Salida esperada
   - Resultado obtenido
3. **Análisis**: No solo pongas capturas, explica qué se probó y por qué
4. **Logs completos**: Muestra la salida del terminal completa

---

## 📧 Contacto

Si tienes dudas sobre las pruebas, revisa:
- `DOCUMENTACION_TECNICA.md` - Sección de pruebas
- `README.md` - Guía general del proyecto

---

**Última actualización**: Noviembre 2025
