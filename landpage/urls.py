from django.urls import path

from . import views

app_name = 'landpage'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('privacidade', views.PoliticaPrivacidadeView.as_view(), name='privacidade'),

    path('ajax/contato', views.ContatoAjaxView.as_view(), name='ajax_contato'),

]
