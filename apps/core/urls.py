"""
Encabezado: Rutas URL para la aplicación Core en demo-sw.
Define las rutas para el home, páginas corporativas en español y robots.txt.
"""
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('conocenos/', views.about_view, name='about'),
    path('politicas/', views.policies_view, name='policies'),
    path('contacto/', views.contact_view, name='contact'),
    path('robots.txt', views.robots_txt_view, name='robots_txt'),
]
