from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView
from vehiculo.views import registro_usuario

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vehiculo.urls')),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('registro/', registro_usuario, name='registro_usuario'),
]

