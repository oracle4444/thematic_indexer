from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(route='', view=include('detector.urls'), name=''),
    path('admin/', admin.site.urls),
]
