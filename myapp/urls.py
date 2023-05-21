from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('info/<int:id>/', views.info, name='info'),
    path('buildinfo/<int:id>/', views.buildinfo, name='buildinfo'),
    path('buildinfo/<int:id_build>/VR/<int:id>/', views.vr, name='VR'),
]