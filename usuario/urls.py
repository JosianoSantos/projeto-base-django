from django.urls import path

from . import views

app_name = 'usuario'

urlpatterns = [
    path('salvar-token-dispositivo-usuario/', views.SalvarTokenDispositivoUsuario.as_view(), name='salvar_token_dispositivo_usuario'),

]
