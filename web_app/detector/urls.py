from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_page, name='start_page'),
    path('detector/', views.detector, name='detector'),
    path('detector/process/', views.process, name='process'),
    path('classes/', views.classes, name='classes'),
    path('classes/<str:class_name>/', views.videos, name='videos'),
    path('classes/<str:class_name>/<str:video_name>/', views.instances, name='instances'),
    path('classes/<str:class_name>/<str:video_name>/<int:instance_id>/', views.video_fragment, name='video_fragment')
]
