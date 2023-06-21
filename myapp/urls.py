from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('info/<int:id>/', views.info, name='info'),
    path('buildinfo/<int:id>/', views.buildinfo, name='buildinfo'),
    path('buildinfo/<int:id_build>/VR/<int:id>/', views.vr, name='VR'),
    path('lk/', views.lk, name='lk'),
    path('lk/redact_data/<int:build_id>/', views.redact_data, name='redact_data'),
    path('userprofile/', views.userprofile, name='userprofile'),
    path('filter/', views.filter, name='filter'),
    path('diagram/', views.diagram, name='diagram'),
    path('lk/redact_data/dop_red', views.redact_data, name='redact_data'),
    path("postuser/", views.postuser, name='postuser'),
    # path('test/', views.test, name='test'), dop_red
]