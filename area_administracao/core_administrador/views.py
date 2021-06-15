from django.views.generic.base import TemplateView

from utils.permissoes_views import LoginRequiredMixin, AdministradorRequiredMixin



class HomeAdministradorView(LoginRequiredMixin, AdministradorRequiredMixin, TemplateView):
    template_name = 'core_administrador/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
