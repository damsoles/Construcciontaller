from django.db import models

# Modelo para almacenar eventos de detección de personas
class PersonCountEvent(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora")
    person_count = models.PositiveIntegerField(default=0, verbose_name="Cantidad de Personas")
    event_id = models.CharField(max_length=50, unique=True, verbose_name="ID del Evento")
    
    class Meta:
        ordering = ['-timestamp']  # Ordenar por fecha descendente
        verbose_name = "Evento de Detección"
        verbose_name_plural = "Eventos de Detección"
    
    def __str__(self):
        return f"ID: {self.event_id} | {self.person_count} persona(s) - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"


# Modelo para tracking individual de personas
class PersonTracking(models.Model):
    person_id = models.CharField(max_length=50, verbose_name="ID de Persona")
    first_seen = models.DateTimeField(auto_now_add=True, verbose_name="Primera Detección")
    last_seen = models.DateTimeField(auto_now=True, verbose_name="Última Detección")
    detection_count = models.PositiveIntegerField(default=1, verbose_name="Veces Detectado")
    
    class Meta:
        ordering = ['-last_seen']
        verbose_name = "Seguimiento de Persona"
        verbose_name_plural = "Seguimiento de Personas"
    
    def __str__(self):
        return f"Persona {self.person_id} - Detectado {self.detection_count} veces"
