# 🚀 Guía de Instalación - Contador de Personas

**⏱️ Tiempo total: 5-10 minutos**

---

## 📋 Requisitos

- **Python 3.8+** instalado → https://www.python.org/downloads/
  - ⚠️ Durante instalación: marca **"Add Python to PATH"**
- **Cámara web** funcionando

---

## 🔧 Instalación (4 Pasos)

### **1. Clonar el Proyecto**

```bash
git clone https://github.com/damsoles/Construcciontaller.git
cd Construcciontaller/contador_personas_lab
```

O descarga el ZIP desde GitHub y descomprímelo.

---

### **2. Crear y Activar Entorno Virtual**

```bash
# Crear
python -m venv venv

# Activar
venv\Scripts\Activate.ps1  # PowerShell
# Si da error: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

✅ Debes ver `(venv)` en tu terminal.

---

### **3. Instalar Dependencias**

```bash
pip install -r requirements.txt
```

⏱️ Tarda 2-5 minutos. Instala Django, OpenCV, numpy, imutils.

**💡 Nota:** El modelo MobileNet-SSD ya está incluido en `detector/models/`

---

### **4. Configurar Base de Datos**

```bash
python manage.py migrate
```

✅ Crea el archivo `db.sqlite3` con las tablas necesarias.

---

## ▶️ Ejecutar el Sistema

```bash
python manage.py runserver
```

Abre tu navegador en: **http://127.0.0.1:8000/**

✅ Verás el video de tu cámara detectando personas en tiempo real.

**Para detener:** `Ctrl+C`

---

## 🌐 URLs del Sistema

- **Aplicación principal:** http://127.0.0.1:8000/
- **API JSON:** http://127.0.0.1:8000/api/events/
- **Admin** (opcional): http://127.0.0.1:8000/admin/

---

## ⚠️ Problemas Comunes

**"python no se reconoce"**
→ Reinstala Python marcando "Add to PATH"

**"ModuleNotFoundError: django"**
→ Activa el entorno virtual: `venv\Scripts\Activate.ps1`

**"PowerShell no permite scripts"**
→ `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

**"Puerto 8000 en uso"**
→ `python manage.py runserver 8080`

**Cámara no funciona**
→ Cierra Zoom/Teams. En Windows: Configuración → Privacidad → Cámara

---

**¡Listo! 🚀**
