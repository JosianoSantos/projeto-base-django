from django.urls import path

from . import views

app_name = 'configuracao'

urlpatterns = [
    path('usuario/listar', views.UsuarioListView.as_view(), name='usuario_list'),
    path('usuario/cadastrar', views.UsuarioCreateView.as_view(), name='usuario_create'),
    path('usuario/<slug:slug>', views.UsuarioUpdateView.as_view(), name='usuario_update'),

    path('informativo/listar', views.NoticiaListView.as_view(), name='noticia_list'),
    path('informativo/cadastrar', views.NoticiaCreateView.as_view(), name='noticia_create'),
    path('informativo/<slug:slug>', views.NoticiaUpdateView.as_view(), name='noticia_update'),

    path('instituicao/listar', views.InstituicaoApoiadoraListView.as_view(), name='instituicao_list'),
    path('instituicao/cadastrar', views.InstituicaoApoiadoraCreateView.as_view(), name='instituicao_create'),
    path('instituicao/<slug:slug>', views.InstituicaoApoiadoraUpdateView.as_view(), name='instituicao_update'),
]
