from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils.decorators import method_decorator


class LoginRequiredMixin(LoginRequiredMixin):
    pass


class AdministradorRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff and request.user.tipo != 'ADMINISTRADOR':
            messages.error(
                request,
                'Área exclusiva para administradores. Você não tem permissão para acessar.')
            return redirect('core:redirecionador')
        return super().dispatch(request, *args, **kwargs)


class EntidadeUsuarioRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        try:
            entidade_usuario = request.session['entidade_usuario']
            return super().dispatch(request, *args, **kwargs)
        except:
            entidades_usuario = request.user.entidades_usuario
            total_entidades_usuario = entidades_usuario.count()
            print(entidades_usuario)
            if total_entidades_usuario == 0:
                messages.error(request, 'Seu usuário não está vinculado a nenhuma Entidade.')
                return redirect('core:redirecionador')
            elif total_entidades_usuario == 1:
                request.session['entidade_usuario'] = entidades_usuario.first()
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect('core_entidade:selecionador_entidade')