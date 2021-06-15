from django.urls import reverse
from django.views.generic.base import RedirectView, TemplateView

from utils.permissoes_views import LoginRequiredMixin


class RedirecionadorView(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        tipo_usuario = self.request.user.tipo
        if tipo_usuario == 'ADMINISTRADOR':
            return reverse('administracao_core:home')
        elif tipo_usuario == 'CLIENTE':
            return reverse('cliente_core:home')
        else:
            return None


class PoliticaPrivacidadeView(TemplateView):
    template_name = 'core/politica_privacidade.html'
