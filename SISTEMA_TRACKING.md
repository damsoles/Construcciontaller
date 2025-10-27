# 🆔 Sistema de Tracking de Personas con ID Único

## 📊 Características Implementadas

### ✅ **Base de Datos SQLite**
- Ubicación: `S:\ConstruccionTaller\contador_personas_lab\db.sqlite3`
- Motor: SQLite3 (nativo de Django)
- Tablas creadas automáticamente

### ✅ **Modelos de Datos**

#### 1. **PersonCountEvent** - Eventos de Detección
```python
- event_id: ID único del evento (formato: EVT-XXXXXXXX)
- person_count: Número de personas detectadas
- timestamp: Fecha y hora exacta de detección (auto)
```

#### 2. **PersonTracking** - Seguimiento Individual (futuro)
```python
- person_id: ID único de persona
- first_seen: Primera vez detectada
- last_seen: Última vez detectada
- detection_count: Veces que fue detectada
```

---

## 🎯 Funcionalidades del Sistema

### **1. Guardado Automático de Eventos**
- Se guarda un evento cada vez que **cambia** el número de personas
- Frecuencia de verificación: cada 30 frames (~1 segundo)
- Cada evento tiene un ID único generado con UUID

### **2. API REST para Frontend**
- **Endpoint**: `http://127.0.0.1:8000/api/events/`
- **Método**: GET
- **Respuesta JSON**:
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

### **3. Frontend Dinámico en Tiempo Real**
- **Actualización automática**: cada 2 segundos vía JavaScript
- **Tabla de historial**: últimos 10 eventos registrados
- **Estadísticas en vivo**: conteo actual y ID del evento activo
- **Diseño profesional**: interfaz moderna con gradientes y animaciones

---

## 🖥️ Interfaz Web

### **Secciones Principales**

#### **📹 Cámara en Vivo** (Columna Izquierda)
- Video streaming con detecciones marcadas
- Rectángulos verdes alrededor de personas
- Contador visible en el video

#### **📊 Estadísticas Actuales** (Columna Izquierda)
- **Personas Detectadas**: Número actual en tiempo real
- **Evento Actual**: ID del evento activo (EVT-XXXXXXXX)

#### **📋 Historial de Detecciones** (Columna Derecha)
- Tabla con 3 columnas:
  - **ID del Evento**: Código único con formato EVT-XXXXXXXX
  - **Personas**: Badge verde con número de personas
  - **Fecha y Hora**: Timestamp completo (YYYY-MM-DD HH:MM:SS)
- Scroll automático si hay más de 10 eventos
- Se actualiza en tiempo real sin recargar la página

---

## 🔧 Flujo de Funcionamiento

```
1. DETECCIÓN → MobileNet-SSD detecta personas en frame
                ↓
2. CONTEO → Cuenta número de personas detectadas
                ↓
3. SUAVIZADO → Buffer de 5 frames para estabilidad
                ↓
4. VERIFICACIÓN → ¿Cambió el conteo?
                ↓ SÍ
5. GUARDADO → Genera UUID → Crea evento en DB
                ↓
6. ACTUALIZACIÓN → Frontend consulta API cada 2s
                ↓
7. VISUALIZACIÓN → Tabla se actualiza automáticamente
```

---

## 📁 Estructura de Archivos Modificados

```
S:\ConstruccionTaller\contador_personas_lab\
│
├── db.sqlite3                          # ← Base de datos con eventos
│
├── detector/
│   ├── models.py                       # ← Modelos PersonCountEvent y PersonTracking
│   ├── views.py                        # ← Lógica de detección y guardado
│   ├── urls.py                         # ← Nueva ruta /api/events/
│   ├── admin.py                        # ← Panel admin de Django
│   │
│   └── templates/detector/
│       └── index.html                  # ← Frontend profesional rediseñado
│
└── detector/migrations/
    └── 0001_initial.py                 # ← Migración de tablas
```

---

## 🚀 Cómo Usar el Sistema

### **Paso 1: Acceder a la Aplicación**
```
http://127.0.0.1:8000/
```

### **Paso 2: Ver Eventos en Tiempo Real**
- La tabla se actualiza automáticamente
- No necesitas recargar la página
- Los eventos se guardan en SQLite

### **Paso 3: Acceder al Panel Admin (Opcional)**
```bash
# Crear superusuario (si no lo has hecho)
python manage.py createsuperuser

# Acceder a:
http://127.0.0.1:8000/admin/
```

En el admin puedes:
- Ver todos los eventos guardados
- Filtrar por fecha y conteo
- Buscar por ID de evento
- Exportar datos

### **Paso 4: Consultar API Directamente**
```
http://127.0.0.1:8000/api/events/
```
Devuelve JSON con los últimos 10 eventos

---

## 💾 Datos en SQLite

### **Ver los Datos Guardados**

#### Opción 1: Desde Python
```python
python manage.py shell

from detector.models import PersonCountEvent
eventos = PersonCountEvent.objects.all()
for e in eventos:
    print(f"{e.event_id} - {e.person_count} personas - {e.timestamp}")
```

#### Opción 2: Django Admin
```
http://127.0.0.1:8000/admin/detector/personcountev
ent/
```

#### Opción 3: DB Browser for SQLite (externo)
- Descargar: https://sqlitebrowser.org/
- Abrir: `db.sqlite3`
- Tabla: `detector_personcountev`

---

## 🎨 Diseño del Frontend

### **Paleta de Colores**
- **Primario**: `#667eea` (Azul violeta)
- **Secundario**: `#764ba2` (Púrpura)
- **Éxito**: `#4CAF50` (Verde)
- **Fondo**: Degradado diagonal

### **Elementos Visuales**
- ✅ Indicador de estado pulsante (verde)
- ✅ Badges tecnológicos (Django, OpenCV, MobileNet-SSD)
- ✅ Cards con sombras 3D
- ✅ Tabla con sticky header
- ✅ Animaciones suaves
- ✅ Responsive design (2 columnas → 1 columna en móvil)

---

## 📈 Próximas Mejoras Sugeridas

1. **Tracking Individual Real**
   - Asignar IDs persistentes a cada persona
   - Usar DeepSORT para seguimiento entre frames
   - Guardar trayectorias

2. **Gráficos de Estadísticas**
   - Chart.js para visualización
   - Gráfico de líneas: personas por hora
   - Gráfico de barras: eventos por día

3. **Alertas y Notificaciones**
   - Email cuando se supere umbral
   - Sonido en el navegador
   - Notificaciones push

4. **Exportación de Datos**
   - Descargar CSV con eventos
   - Generar reportes PDF
   - Integración con Excel

5. **Análisis Avanzado**
   - Tiempo promedio de permanencia
   - Horas pico de detección
   - Comparación día vs noche

---

## ✅ Lista de Verificación

- [x] Modelo PersonCountEvent creado
- [x] Modelo PersonTracking creado
- [x] Migraciones aplicadas
- [x] Lógica de guardado implementada
- [x] API endpoint funcionando
- [x] Frontend rediseñado
- [x] Actualización en tiempo real con JavaScript
- [x] Admin de Django configurado
- [x] Sistema probado y funcionando

---

## 🎯 Resultado Final

**¡Sistema completo de tracking con ID único funcionando!**

✅ Cada detección tiene un evento con ID único (EVT-XXXXXXXX)  
✅ Fecha y hora se guardan automáticamente  
✅ Frontend profesional muestra datos en tiempo real  
✅ Base de datos SQLite almacena todo persistentemente  
✅ API REST disponible para consultas  

**¡Listo para usar en producción! 🚀**
