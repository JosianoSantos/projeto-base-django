from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.RedirecionadorView.as_view(), name='redirecionador'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('privacidade', views.PoliticaPrivacidadeView.as_view(), name='privacidade'),

    path('alterar-senha/', auth_views.PasswordChangeView.as_view(template_name='core/senha/alterar_senha.html',
                                                                 success_url=reverse_lazy('core:password_change_done')
                                                                 ), name='password_change'),
    path('alterar-senha-confirmacao/',
         auth_views.PasswordChangeDoneView.as_view(template_name='core/senha/sucesso_confirmacao.html'),
         name='password_change_done'),

    path('esqueci-senha/', auth_views.PasswordResetView.as_view(template_name='core/senha/resetar_senha.html',
                                                                html_email_template_name='core/senha/email_reset_senha.html',
                                                                success_url=reverse_lazy('core:password_reset_done')),
         name='password_reset'),
    path('resetar-senha-sucesso/', auth_views.PasswordResetDoneView.as_view(
        template_name='core/senha/resetar_senha_resposta.html'),
         name='password_reset_done'),
    path('resetar-senha-completo/',
         auth_views.PasswordResetCompleteView.as_view(template_name='core/senha/sucesso_confirmacao.html'),
         name='password_reset_complete'),

]
