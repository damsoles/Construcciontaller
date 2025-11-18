"""
PRUEBAS DE INTEGRACIÓN - RUTAS PRINCIPALES DE DJANGO
=====================================================
Archivo: test_django_integration.py
Descripción: Pruebas de integración para validar el flujo completo de la aplicación
            Django (autenticación, rutas protegidas, API)

Autor: Sistema de Detección de Personas
Fecha: Noviembre 2025
"""

import unittest
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'people_counter.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from detector.models import PersonCountEvent, PersonTracking


class TestAutenticacion(TestCase):
    """
    Pruebas de integración para el sistema de autenticación
    """
    
    def setUp(self):
        """Configuración inicial: crear cliente HTTP y usuario de prueba"""
        self.client = Client()
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_01_acceso_login_sin_autenticar(self):
        """
        Caso de Prueba #1: Acceso a página de login sin autenticación
        
        Objetivo: Verificar que la página de login es accesible públicamente
        Entrada: GET request a /login/
        Salida esperada: Status 200, página de login visible
        """
        print("\n[TEST 1] Accediendo a página de login sin autenticación...")
        
        response = self.client.get(reverse('login'))
        
        self.assertEqual(response.status_code, 200, "Login debería ser accesible")
        self.assertContains(response, 'Sistema de Detección de Personas')
        self.assertContains(response, 'Iniciar Sesión')
        
        print("   Status Code: 200")
        print("   Contenido: Página de login renderizada correctamente")
        print("✅ PASÓ: Login accesible sin autenticación")
    
    def test_02_acceso_registro_sin_autenticar(self):
        """
        Caso de Prueba #2: Acceso a página de registro sin autenticación
        
        Objetivo: Verificar que la página de registro es accesible públicamente
        Entrada: GET request a /register/
        Salida esperada: Status 200, formulario de registro visible
        """
        print("\n[TEST 2] Accediendo a página de registro...")
        
        response = self.client.get(reverse('register'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Crear Nueva Cuenta')
        
        print("   Status Code: 200")
        print("✅ PASÓ: Registro accesible")
    
    def test_03_acceso_index_sin_autenticar(self):
        """
        Caso de Prueba #3: Acceso a index sin autenticación
        
        Objetivo: Verificar que la página principal redirige a login si no está autenticado
        Entrada: GET request a / sin sesión activa
        Salida esperada: Status 302 (redirección a /login/)
        """
        print("\n[TEST 3] Intentando acceder a index sin autenticación...")
        
        response = self.client.get(reverse('index'))
        
        self.assertEqual(response.status_code, 302, "Debería redirigir")
        self.assertIn('/login/', response.url, "Debería redirigir a login")
        
        print(f"   Status Code: 302 (Redirección)")
        print(f"   Redirige a: {response.url}")
        print("✅ PASÓ: Index protegido correctamente")
    
    def test_04_login_credenciales_validas(self):
        """
        Caso de Prueba #4: Login con credenciales correctas
        
        Objetivo: Validar el flujo de autenticación exitoso
        Entrada: POST a /login/ con username='testuser', password='testpass123'
        Salida esperada: Status 302 (redirección a index), usuario autenticado
        """
        print("\n[TEST 4] Probando login con credenciales válidas...")
        
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        
        self.assertEqual(response.status_code, 302, "Debería redirigir después de login")
        self.assertEqual(response.url, reverse('index'), "Debería redirigir a index")
        
        # Verificar que el usuario está autenticado
        self.assertTrue(
            '_auth_user_id' in self.client.session,
            "Usuario debería estar autenticado"
        )
        
        print("   Status Code: 302")
        print(f"   Redirige a: {response.url}")
        print("   Usuario autenticado: Sí")
        print("✅ PASÓ: Login exitoso")
    
    def test_05_login_credenciales_invalidas(self):
        """
        Caso de Prueba #5: Login con credenciales incorrectas
        
        Objetivo: Verificar manejo de errores en autenticación
        Entrada: POST a /login/ con password incorrecta
        Salida esperada: Status 200 (misma página), mensaje de error
        """
        print("\n[TEST 5] Probando login con credenciales inválidas...")
        
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        
        self.assertEqual(response.status_code, 200, "Debería mostrar página de login")
        self.assertContains(response, 'Usuario o contraseña incorrectos')
        
        print("   Status Code: 200 (sin redirección)")
        print("   Mensaje de error mostrado: Sí")
        print("✅ PASÓ: Error de login manejado correctamente")
    
    def test_06_registro_usuario_valido(self):
        """
        Caso de Prueba #6: Registro de nuevo usuario con datos válidos
        
        Objetivo: Validar creación de nuevo usuario
        Entrada: POST a /register/ con datos válidos
        Salida esperada: Usuario creado, redirección a login
        """
        print("\n[TEST 6] Registrando nuevo usuario...")
        
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123'
        })
        
        self.assertEqual(response.status_code, 302, "Debería redirigir después de registro")
        
        # Verificar que el usuario fue creado
        user_exists = User.objects.filter(username='newuser').exists()
        self.assertTrue(user_exists, "Usuario debería estar creado en la BD")
        
        print("   Status Code: 302")
        print("   Usuario creado: Sí")
        print("✅ PASÓ: Registro exitoso")
    
    def test_07_registro_contrasenas_no_coinciden(self):
        """
        Caso de Prueba #7: Registro con contraseñas que no coinciden
        
        Objetivo: Verificar validación de contraseñas
        Entrada: POST con password1 != password2
        Salida esperada: Error mostrado, usuario no creado
        """
        print("\n[TEST 7] Intentando registro con contraseñas diferentes...")
        
        response = self.client.post(reverse('register'), {
            'username': 'baduser',
            'email': 'bad@example.com',
            'password1': 'pass123',
            'password2': 'pass456'
        })
        
        self.assertEqual(response.status_code, 200, "Debería mostrar formulario con error")
        self.assertContains(response, 'Las contraseñas no coinciden')
        
        # Verificar que el usuario NO fue creado
        user_exists = User.objects.filter(username='baduser').exists()
        self.assertFalse(user_exists, "Usuario no debería existir")
        
        print("   Mensaje de error mostrado: Sí")
        print("   Usuario creado: No")
        print("✅ PASÓ: Validación de contraseñas correcta")


class TestRutasProtegidas(TestCase):
    """
    Pruebas de integración para rutas que requieren autenticación
    """
    
    def setUp(self):
        """Configuración: crear usuario y cliente"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='authuser',
            password='authpass123'
        )
    
    def test_08_acceso_index_autenticado(self):
        """
        Caso de Prueba #8: Acceso a index con usuario autenticado
        
        Objetivo: Verificar que usuarios autenticados pueden acceder al sistema
        Entrada: GET a / con sesión activa
        Salida esperada: Status 200, dashboard visible
        """
        print("\n[TEST 8] Accediendo a index con autenticación...")
        
        # Autenticar usuario
        self.client.login(username='authuser', password='authpass123')
        
        response = self.client.get(reverse('index'))
        
        self.assertEqual(response.status_code, 200, "Index debería ser accesible")
        self.assertContains(response, 'Conteo de personas en el laboratorio')
        self.assertContains(response, 'Iniciar Cámara')
        
        print("   Status Code: 200")
        print("   Dashboard cargado: Sí")
        print("✅ PASÓ: Acceso autorizado al index")
    
    def test_09_acceso_video_feed_autenticado(self):
        """
        Caso de Prueba #9: Acceso al streaming de video
        
        Objetivo: Verificar que la ruta de video requiere autenticación
        Entrada: GET a /video_feed/
        Salida esperada: Status 200 o redirección según autenticación
        """
        print("\n[TEST 9] Accediendo a video_feed...")
        
        # Autenticar
        self.client.login(username='authuser', password='authpass123')
        
        response = self.client.get(reverse('video_feed'))
        
        # El status puede ser 200 (streaming) o error si no hay cámara
        # Lo importante es que no sea 302 (redirección a login)
        self.assertNotEqual(response.status_code, 302, "No debería redirigir con autenticación")
        
        print(f"   Status Code: {response.status_code}")
        print("✅ PASÓ: Video feed accesible con autenticación")
    
    def test_10_logout(self):
        """
        Caso de Prueba #10: Cierre de sesión
        
        Objetivo: Verificar que logout cierra la sesión correctamente
        Entrada: GET a /logout/
        Salida esperada: Sesión cerrada, redirección a login
        """
        print("\n[TEST 10] Probando cierre de sesión...")
        
        # Primero hacer login
        self.client.login(username='authuser', password='authpass123')
        
        # Verificar que está autenticado
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200, "Debería estar autenticado")
        
        # Hacer logout
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302, "Debería redirigir")
        
        # Verificar que ya no puede acceder al index
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302, "No debería estar autenticado")
        
        print("   Logout exitoso: Sí")
        print("   Sesión cerrada: Sí")
        print("✅ PASÓ: Logout funcionando correctamente")


class TestAPI(TestCase):
    """
    Pruebas de integración para los endpoints de la API REST
    """
    
    def setUp(self):
        """Configuración: crear usuario y eventos de prueba"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='apiuser',
            password='apipass123'
        )
        
        # Crear eventos de prueba
        PersonCountEvent.objects.create(
            event_id='EVT-TEST001',
            person_count=2
        )
        PersonCountEvent.objects.create(
            event_id='EVT-TEST002',
            person_count=3
        )
    
    def test_11_api_eventos_sin_autenticacion(self):
        """
        Caso de Prueba #11: Acceso a API sin autenticación
        
        Objetivo: Verificar que la API requiere autenticación
        Entrada: GET a /api/events/ sin sesión
        Salida esperada: Status 302 (redirección a login)
        """
        print("\n[TEST 11] Intentando acceder a API sin autenticación...")
        
        response = self.client.get(reverse('get_recent_events'))
        
        self.assertEqual(response.status_code, 302, "API debería requerir login")
        
        print("   Status Code: 302 (redirige a login)")
        print("✅ PASÓ: API protegida correctamente")
    
    def test_12_api_eventos_autenticado(self):
        """
        Caso de Prueba #12: Acceso a API con autenticación
        
        Objetivo: Verificar que la API devuelve datos JSON correctos
        Entrada: GET a /api/events/ con sesión activa
        Salida esperada: Status 200, JSON con estructura correcta
        """
        print("\n[TEST 12] Accediendo a API con autenticación...")
        
        self.client.login(username='apiuser', password='apipass123')
        
        response = self.client.get(reverse('get_recent_events'))
        
        self.assertEqual(response.status_code, 200, "API debería responder")
        self.assertEqual(
            response['Content-Type'],
            'application/json',
            "Respuesta debería ser JSON"
        )
        
        # Verificar estructura de datos
        data = response.json()
        self.assertIn('events', data, "JSON debería tener 'events'")
        self.assertIn('current_count', data, "JSON debería tener 'current_count'")
        self.assertIn('current_event_id', data, "JSON debería tener 'current_event_id'")
        
        print("   Status Code: 200")
        print(f"   Eventos devueltos: {len(data['events'])}")
        print(f"   Estructura JSON: ✓ events, ✓ current_count, ✓ current_event_id")
        print("✅ PASÓ: API funcionando correctamente")
    
    def test_13_api_stop_camera(self):
        """
        Caso de Prueba #13: Endpoint para detener cámara
        
        Objetivo: Verificar que el endpoint de detener cámara funciona
        Entrada: POST a /api/stop_camera/
        Salida esperada: Status 200, JSON con status
        """
        print("\n[TEST 13] Probando endpoint de detener cámara...")
        
        self.client.login(username='apiuser', password='apipass123')
        
        response = self.client.get(reverse('stop_camera'))
        
        self.assertEqual(response.status_code, 200, "Endpoint debería responder")
        
        data = response.json()
        self.assertIn('status', data, "Respuesta debería tener 'status'")
        
        print("   Status Code: 200")
        print(f"   Respuesta: {data}")
        print("✅ PASÓ: Endpoint stop_camera funcionando")


class TestFlujoCompleto(TestCase):
    """
    Pruebas de integración end-to-end del flujo completo
    """
    
    def test_14_flujo_completo_usuario(self):
        """
        Caso de Prueba #14: Flujo completo de usuario
        
        Objetivo: Simular el flujo completo desde registro hasta uso de la aplicación
        Pasos:
            1. Registrar nuevo usuario
            2. Hacer login
            3. Acceder al dashboard
            4. Consultar API de eventos
            5. Hacer logout
        Salida esperada: Todos los pasos exitosos
        """
        print("\n[TEST 14] Ejecutando flujo completo de usuario...")
        
        # PASO 1: Registro
        print("   [1/5] Registrando usuario...")
        response = self.client.post(reverse('register'), {
            'username': 'flowuser',
            'email': 'flow@example.com',
            'password1': 'flowpass123',
            'password2': 'flowpass123'
        })
        self.assertEqual(response.status_code, 302, "Registro debería redirigir")
        print("      ✓ Usuario registrado")
        
        # PASO 2: Login
        print("   [2/5] Iniciando sesión...")
        response = self.client.post(reverse('login'), {
            'username': 'flowuser',
            'password': 'flowpass123'
        })
        self.assertEqual(response.status_code, 302, "Login debería redirigir")
        print("      ✓ Sesión iniciada")
        
        # PASO 3: Acceder a dashboard
        print("   [3/5] Accediendo al dashboard...")
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200, "Dashboard debería cargar")
        print("      ✓ Dashboard cargado")
        
        # PASO 4: Consultar API
        print("   [4/5] Consultando API de eventos...")
        response = self.client.get(reverse('get_recent_events'))
        self.assertEqual(response.status_code, 200, "API debería responder")
        data = response.json()
        self.assertIn('events', data)
        print("      ✓ API respondió correctamente")
        
        # PASO 5: Logout
        print("   [5/5] Cerrando sesión...")
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302, "Logout debería redirigir")
        
        # Verificar que ya no puede acceder
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302, "No debería tener acceso")
        print("      ✓ Sesión cerrada")
        
        print("\n✅ PASÓ: Flujo completo ejecutado exitosamente")


class TestModelos(TestCase):
    """
    Pruebas de integración para los modelos de base de datos
    """
    
    def test_15_crear_evento_conteo(self):
        """
        Caso de Prueba #15: Crear evento de conteo en BD
        
        Objetivo: Verificar que se pueden crear registros en PersonCountEvent
        Entrada: Datos de evento (event_id, person_count)
        Salida esperada: Registro creado exitosamente
        """
        print("\n[TEST 15] Creando evento de conteo en base de datos...")
        
        evento = PersonCountEvent.objects.create(
            event_id='EVT-TEST999',
            person_count=5
        )
        
        self.assertEqual(evento.person_count, 5)
        self.assertEqual(evento.event_id, 'EVT-TEST999')
        self.assertIsNotNone(evento.timestamp)
        
        # Verificar que se guardó en la BD
        evento_bd = PersonCountEvent.objects.get(event_id='EVT-TEST999')
        self.assertEqual(evento_bd.person_count, 5)
        
        print(f"   Event ID: {evento.event_id}")
        print(f"   Person Count: {evento.person_count}")
        print(f"   Timestamp: {evento.timestamp}")
        print("✅ PASÓ: Evento creado correctamente")
    
    def test_16_consultar_eventos_recientes(self):
        """
        Caso de Prueba #16: Consultar últimos eventos
        
        Objetivo: Verificar query de últimos 10 eventos
        Entrada: Query PersonCountEvent.objects.all()[:10]
        Salida esperada: Lista de eventos ordenados por fecha
        """
        print("\n[TEST 16] Consultando eventos recientes...")
        
        # Crear varios eventos
        for i in range(15):
            PersonCountEvent.objects.create(
                event_id=f'EVT-{i:08d}',
                person_count=i % 5
            )
        
        # Consultar últimos 10
        eventos = PersonCountEvent.objects.all()[:10]
        
        self.assertEqual(len(eventos), 10, "Debería devolver 10 eventos")
        
        print(f"   Total eventos en BD: {PersonCountEvent.objects.count()}")
        print(f"   Eventos consultados: {len(eventos)}")
        print("✅ PASÓ: Query de eventos funciona")


# Punto de entrada para ejecutar las pruebas
if __name__ == '__main__':
    print("="*70)
    print("  PRUEBAS DE INTEGRACIÓN - RUTAS PRINCIPALES DE DJANGO")
    print("="*70)
    print("\nDescripción: Validación del flujo completo de la aplicación")
    print("Módulo: Django (autenticación, rutas, API, modelos)")
    print("\n" + "="*70 + "\n")
    
    # Ejecutar pruebas con verbosidad
    unittest.main(verbosity=2)
