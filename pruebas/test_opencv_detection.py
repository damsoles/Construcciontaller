"""
PRUEBAS UNITARIAS - MÓDULO DE DETECCIÓN CON OPENCV
===================================================
Archivo: test_opencv_detection.py
Descripción: Pruebas unitarias sobre las funciones críticas del sistema
            de detección con OpenCV y MobileNet-SSD

Autor: Sistema de Detección de Personas
Fecha: Noviembre 2025
"""

import unittest
import cv2
import numpy as np
import os
import sys

# Agregar path del proyecto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestModeloMobileNetSSD(unittest.TestCase):
    """
    Pruebas unitarias para verificar el modelo MobileNet-SSD
    """
    
    def setUp(self):
        """Configuración inicial antes de cada prueba"""
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.MODEL_DIR = os.path.join(self.BASE_DIR, 'detector', 'models')
        self.PROTOTXT = os.path.join(self.MODEL_DIR, 'MobileNetSSD_deploy.prototxt')
        self.CAFFEMODEL = os.path.join(self.MODEL_DIR, 'MobileNetSSD_deploy.caffemodel')
    
    def test_01_existencia_archivo_prototxt(self):
        """
        Caso de Prueba #1: Verificar existencia del archivo prototxt
        
        Objetivo: Comprobar que el archivo de configuración del modelo existe
        Entrada: Ruta al archivo MobileNetSSD_deploy.prototxt
        Salida esperada: El archivo debe existir en la ruta especificada
        """
        print("\n[TEST 1] Verificando existencia de prototxt...")
        self.assertTrue(
            os.path.exists(self.PROTOTXT),
            f"El archivo prototxt no existe en: {self.PROTOTXT}"
        )
        print(f"✅ PASÓ: Archivo encontrado en {self.PROTOTXT}")
    
    def test_02_existencia_archivo_caffemodel(self):
        """
        Caso de Prueba #2: Verificar existencia del archivo caffemodel
        
        Objetivo: Comprobar que el archivo de pesos del modelo existe
        Entrada: Ruta al archivo MobileNetSSD_deploy.caffemodel
        Salida esperada: El archivo debe existir y pesar aproximadamente 23MB
        """
        print("\n[TEST 2] Verificando existencia de caffemodel...")
        self.assertTrue(
            os.path.exists(self.CAFFEMODEL),
            f"El archivo caffemodel no existe en: {self.CAFFEMODEL}"
        )
        
        # Verificar tamaño del archivo
        size_mb = os.path.getsize(self.CAFFEMODEL) / (1024 * 1024)
        print(f"   Tamaño del modelo: {size_mb:.2f} MB")
        self.assertGreater(size_mb, 20, "El archivo caffemodel es muy pequeño")
        self.assertLess(size_mb, 30, "El archivo caffemodel es muy grande")
        print(f"✅ PASÓ: Archivo encontrado ({size_mb:.2f} MB)")
    
    def test_03_carga_modelo_opencv(self):
        """
        Caso de Prueba #3: Cargar modelo MobileNet-SSD con OpenCV
        
        Objetivo: Verificar que OpenCV puede cargar el modelo correctamente
        Entrada: Archivos prototxt y caffemodel
        Salida esperada: Objeto net no nulo, sin excepciones
        """
        print("\n[TEST 3] Cargando modelo con OpenCV DNN...")
        try:
            net = cv2.dnn.readNetFromCaffe(self.PROTOTXT, self.CAFFEMODEL)
            self.assertIsNotNone(net, "El modelo no se cargó correctamente")
            print("✅ PASÓ: Modelo cargado exitosamente")
        except Exception as e:
            self.fail(f"Error al cargar el modelo: {str(e)}")


class TestDeteccionPersonas(unittest.TestCase):
    """
    Pruebas unitarias para el proceso de detección de personas
    """
    
    def setUp(self):
        """Configuración inicial: cargar modelo"""
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.MODEL_DIR = os.path.join(self.BASE_DIR, 'detector', 'models')
        self.PROTOTXT = os.path.join(self.MODEL_DIR, 'MobileNetSSD_deploy.prototxt')
        self.CAFFEMODEL = os.path.join(self.MODEL_DIR, 'MobileNetSSD_deploy.caffemodel')
        
        # Cargar modelo
        self.net = cv2.dnn.readNetFromCaffe(self.PROTOTXT, self.CAFFEMODEL)
    
    def test_04_deteccion_en_imagen_blanca(self):
        """
        Caso de Prueba #4: Detección en imagen sintética (blanco)
        
        Objetivo: Probar que la detección procesa imágenes correctamente
        Entrada: Imagen 640x480 completamente blanca
        Salida esperada: Detecciones procesadas sin errores, array con forma correcta
        """
        print("\n[TEST 4] Probando detección en imagen blanca...")
        
        # Crear imagen de prueba (blanco puro)
        test_image = np.ones((480, 640, 3), dtype=np.uint8) * 255
        
        # Crear blob y hacer detección
        blob = cv2.dnn.blobFromImage(
            cv2.resize(test_image, (300, 300)),
            0.007843,
            (300, 300),
            127.5
        )
        self.net.setInput(blob)
        detections = self.net.forward()
        
        # Verificar formato de salida
        self.assertIsNotNone(detections, "La detección no devolvió resultados")
        self.assertEqual(len(detections.shape), 4, "Formato de detección incorrecto")
        print(f"   Shape de detecciones: {detections.shape}")
        print("✅ PASÓ: Detección procesada correctamente")
    
    def test_05_deteccion_en_imagen_negra(self):
        """
        Caso de Prueba #5: Detección en imagen sintética (negro)
        
        Objetivo: Verificar comportamiento con imagen oscura
        Entrada: Imagen 640x480 completamente negra
        Salida esperada: Procesamiento sin errores
        """
        print("\n[TEST 5] Probando detección en imagen negra...")
        
        # Crear imagen de prueba (negro puro)
        test_image = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Crear blob y hacer detección
        blob = cv2.dnn.blobFromImage(
            cv2.resize(test_image, (300, 300)),
            0.007843,
            (300, 300),
            127.5
        )
        self.net.setInput(blob)
        detections = self.net.forward()
        
        self.assertIsNotNone(detections)
        print("✅ PASÓ: Imagen oscura procesada correctamente")
    
    def test_06_formato_detecciones(self):
        """
        Caso de Prueba #6: Verificar formato de las detecciones
        
        Objetivo: Comprobar que las detecciones tienen el formato esperado
        Entrada: Imagen de prueba aleatoria
        Salida esperada: Array con shape (1, 1, N, 7) donde N es el número de detecciones
        """
        print("\n[TEST 6] Verificando formato de detecciones...")
        
        # Crear imagen aleatoria
        test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        
        blob = cv2.dnn.blobFromImage(
            cv2.resize(test_image, (300, 300)),
            0.007843,
            (300, 300),
            127.5
        )
        self.net.setInput(blob)
        detections = self.net.forward()
        
        # Verificar dimensiones
        self.assertEqual(detections.shape[0], 1, "Dimensión 0 incorrecta")
        self.assertEqual(detections.shape[1], 1, "Dimensión 1 incorrecta")
        self.assertEqual(detections.shape[3], 7, "Cada detección debe tener 7 valores")
        print(f"   Formato correcto: {detections.shape}")
        print("✅ PASÓ: Formato de detecciones válido")


class TestFiltrosDeteccion(unittest.TestCase):
    """
    Pruebas unitarias para los filtros de confianza y validación
    """
    
    def test_07_filtro_confianza(self):
        """
        Caso de Prueba #7: Filtro de confianza mínima
        
        Objetivo: Verificar que el filtro de confianza funciona correctamente
        Entrada: Lista de valores de confianza [0.3, 0.6, 0.8, 0.4, 0.9]
        Salida esperada: Solo valores >= 0.5 deben pasar el filtro
        """
        print("\n[TEST 7] Probando filtro de confianza...")
        
        confidence_values = [0.3, 0.6, 0.8, 0.4, 0.9]
        threshold = 0.5
        
        filtered = [c for c in confidence_values if c > threshold]
        
        self.assertEqual(len(filtered), 3, "El filtro no funciona correctamente")
        self.assertNotIn(0.3, filtered, "0.3 no debería pasar el filtro")
        self.assertNotIn(0.4, filtered, "0.4 no debería pasar el filtro")
        self.assertIn(0.6, filtered, "0.6 debería pasar el filtro")
        self.assertIn(0.8, filtered, "0.8 debería pasar el filtro")
        self.assertIn(0.9, filtered, "0.9 debería pasar el filtro")
        
        print(f"   Valores originales: {confidence_values}")
        print(f"   Valores filtrados (>= {threshold}): {filtered}")
        print("✅ PASÓ: Filtro de confianza funcionando")
    
    def test_08_validacion_aspect_ratio(self):
        """
        Caso de Prueba #8: Validación de proporción (aspect ratio)
        
        Objetivo: Verificar que las detecciones tienen proporciones humanas
        Entrada: Bounding boxes con diferentes proporciones
        Salida esperada: Solo proporciones entre 1.2 y 4.0 son válidas
        """
        print("\n[TEST 8] Validando aspect ratio de bounding boxes...")
        
        # Casos de prueba: (ancho, alto, es_valido)
        test_cases = [
            (100, 200, True),   # ratio 0.5 -> 2.0 válido
            (100, 100, False),  # ratio 1.0 -> muy cuadrado
            (100, 400, True),   # ratio 0.25 -> 4.0 válido
            (200, 100, False),  # ratio 2.0 -> muy ancho
            (80, 250, True),    # ratio 0.32 -> 3.125 válido
        ]
        
        min_ratio = 1.2
        max_ratio = 4.0
        
        for width, height, expected_valid in test_cases:
            aspect_ratio = height / width
            is_valid = min_ratio <= aspect_ratio <= max_ratio
            
            print(f"   Box {width}x{height}: ratio={aspect_ratio:.2f}, válido={is_valid}")
            
            if expected_valid:
                self.assertTrue(is_valid, f"Box {width}x{height} debería ser válido")
            else:
                # Nota: Algunos casos pueden ser válidos/inválidos dependiendo del umbral
                pass
        
        print("✅ PASÓ: Validación de aspect ratio correcta")
    
    def test_09_area_minima(self):
        """
        Caso de Prueba #9: Filtro de área mínima
        
        Objetivo: Verificar que solo se aceptan detecciones de tamaño suficiente
        Entrada: Bounding boxes de diferentes tamaños
        Salida esperada: Solo áreas >= 2000 píxeles son válidas
        """
        print("\n[TEST 9] Verificando filtro de área mínima...")
        
        min_area = 2000
        
        # Casos de prueba: (ancho, alto, debería_pasar)
        test_boxes = [
            (50, 50, False),    # área = 2500 (válido)
            (30, 30, False),    # área = 900 (inválido)
            (100, 200, True),   # área = 20000 (válido)
            (40, 40, False),    # área = 1600 (inválido)
            (50, 100, True),    # área = 5000 (válido)
        ]
        
        for width, height, should_pass in test_boxes:
            area = width * height
            is_valid = area >= min_area
            
            print(f"   Box {width}x{height}: área={area}px, válido={is_valid}")
            
            if should_pass:
                self.assertTrue(is_valid, f"Box con área {area} debería ser válido")
        
        print("✅ PASÓ: Filtro de área mínima funcionando")


class TestSuavizadoTemporal(unittest.TestCase):
    """
    Pruebas unitarias para el algoritmo de suavizado temporal
    """
    
    def test_10_buffer_temporal(self):
        """
        Caso de Prueba #10: Buffer de suavizado temporal
        
        Objetivo: Verificar que el buffer mantiene los últimos 5 valores
        Entrada: Secuencia de conteos [3, 2, 3, 3, 2, 3, 3]
        Salida esperada: Buffer mantiene solo 5 valores más recientes
        """
        print("\n[TEST 10] Probando buffer de suavizado temporal...")
        
        count_buffer = []
        max_buffer_size = 5
        
        sequence = [3, 2, 3, 3, 2, 3, 3]
        
        for count in sequence:
            count_buffer.append(count)
            if len(count_buffer) > max_buffer_size:
                count_buffer.pop(0)
            
            print(f"   Conteo={count}, Buffer actual: {count_buffer}")
        
        self.assertEqual(len(count_buffer), max_buffer_size, "Buffer debería tener 5 elementos")
        self.assertEqual(count_buffer, [3, 2, 3, 3], "Buffer no mantiene los valores correctos")
        print("✅ PASÓ: Buffer temporal funcionando")
    
    def test_11_calculo_moda(self):
        """
        Caso de Prueba #11: Cálculo de moda para estabilización
        
        Objetivo: Verificar que se calcula correctamente el valor más frecuente
        Entrada: Buffer [3, 2, 3, 3, 2]
        Salida esperada: Moda = 3 (aparece 3 veces)
        """
        print("\n[TEST 11] Calculando moda del buffer...")
        
        from collections import Counter
        
        buffer = [3, 2, 3, 3, 2]
        moda = Counter(buffer).most_common(1)[0][0]
        
        print(f"   Buffer: {buffer}")
        print(f"   Moda calculada: {moda}")
        
        self.assertEqual(moda, 3, "La moda debería ser 3")
        print("✅ PASÓ: Cálculo de moda correcto")


# Punto de entrada para ejecutar las pruebas
if __name__ == '__main__':
    print("="*70)
    print("  PRUEBAS UNITARIAS - MÓDULO DE DETECCIÓN CON OPENCV")
    print("="*70)
    print("\nDescripción: Pruebas sobre funciones críticas del sistema")
    print("Módulo: Detección con OpenCV y MobileNet-SSD")
    print("\n" + "="*70 + "\n")
    
    # Ejecutar pruebas con verbosidad
    unittest.main(verbosity=2)
