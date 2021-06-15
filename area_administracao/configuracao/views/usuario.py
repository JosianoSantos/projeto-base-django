from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from area_administracao.configuracao.forms import UsuarioForm, UsuarioUpdateForm
from usuario.models import Usuario
from utils.permissoes_views import LoginRequiredMixin, AdministradorRequiredMixin


class UsuarioListView(LoginRequiredMixin, AdministradorRequiredMixin, ListView):
    template_name = 'configuracao/usuario/list.html'
    model = Usuario

    def get_queryset(self):
        return Usuario.objects.filter(nome__icontains=self.request.GET.get('busca') or '')


class UsuarioCreateView(LoginRequiredMixin, AdministradorRequiredMixin, CreateView):
    template_name = 'configuracao/usuario/form.html'
    model = Usuario
    form_class = UsuarioForm
    success_url = reverse_lazy('configuracao:usuario_list')

    def form_valid(self, form):
        usuario = form.save(commit=False)
        usuario.set_password(form.cleaned_data['password'])
        usuario.save()
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Usuário cadastrado com sucesso!')
        return self.success_url


class UsuarioUpdateView(LoginRequiredMixin, AdministradorRequiredMixin, UpdateView):
    template_name = 'configuracao/usuario/form.html'
    model = Usuario
    form_class = UsuarioUpdateForm
    success_url = reverse_lazy('configuracao:usuario_list')

    def get_success_url(self):
        messages.success(self.request, 'Usuário atualizado com sucesso.')
        return self.success_url
