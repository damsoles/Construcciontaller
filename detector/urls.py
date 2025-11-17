from django.urls import path
from . import views

urlpatterns = [
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Aplicación principal (requiere login)
    path('', views.index, name='index'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('api/events/', views.get_recent_events, name='get_recent_events'),
    path('api/stop_camera/', views.stop_camera, name='stop_camera'),
]
