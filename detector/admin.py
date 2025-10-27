from django.contrib import admin
from .models import PersonCountEvent, PersonTracking

@admin.register(PersonCountEvent)
class PersonCountEventAdmin(admin.ModelAdmin):
    list_display = ('event_id', 'person_count', 'timestamp')
    list_filter = ('timestamp', 'person_count')
    search_fields = ('event_id',)
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)

@admin.register(PersonTracking)
class PersonTrackingAdmin(admin.ModelAdmin):
    list_display = ('person_id', 'detection_count', 'first_seen', 'last_seen')
    list_filter = ('first_seen', 'last_seen')
    search_fields = ('person_id',)
    ordering = ('-last_seen',)
    readonly_fields = ('first_seen', 'last_seen')
