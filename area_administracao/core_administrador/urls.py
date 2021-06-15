from django.urls import path

from . import views

app_name = 'core_administrador'

urlpatterns = [
    path('home', views.HomeAdministradorView.as_view(), name='home'),
]
