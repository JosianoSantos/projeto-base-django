import requests
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.http import JsonResponse
from django.template.loader import get_template
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'landpage/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PoliticaPrivacidadeView(TemplateView):
    template_name = 'landpage/politica_privacidade.html'


class ContatoAjaxView(View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(ContatoAjaxView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        nome = self.request.POST.get('nome')
        email = self.request.POST.get('email')
        telefone = self.request.POST.get('telefone')
        assunto = self.request.POST.get('assunto')
        mensagem = self.request.POST.get('mensagem')

        error_messages = {}
        if not nome:
            error_messages['nome'] = 'O nome é obrigatório.'

        if not email:
            error_messages['email'] = 'O E-Mail é obrigatório.'

        if not mensagem:
            error_messages['mensagem'] = 'A mensagem é obrigatória.'

        if not telefone:
            error_messages['telefone'] = 'O telefone é obrigatório.'

        if not assunto:
            error_messages['assunto'] = 'O assunto é obrigatório.'

        try:
            validate_email(email)
        except:
            error_messages['email'] = 'Email inválido.'

        if not check_captcha(self.request.POST.get('g_recaptcha_response')):
            error_messages['recaptcha'] = 'Não foi possível verificar o reCaptcha, tente novamente.'

        success = False
        if len(error_messages) == 0:
            if enviar_email_contato(nome, email, telefone, assunto, mensagem):
                Contato.objects.create(nome=nome, email=email, telefone=telefone, assunto=assunto, mensagem=mensagem)
                success = True
            else:
                success = False

        return JsonResponse(data={
            'success': success,
            'error_messages': error_messages
        }, status=200)


def check_captcha(recaptcha_response):
    try:
        requisicao = requests.request(method='POST', url='https://www.google.com/recaptcha/api/siteverify',
                                      data={'secret': '6LcGs9oZAAAAAFJfEkkkFZY03q6sirJ12Cd9vPFe',
                                            'response': recaptcha_response})

        if requisicao.json()['success']:
            return True
        else:
            return False

    except Exception as e:
        return False


def enviar_email_contato(nome, email, telefone, assunto, mensagem):
    context = {
        'nome': nome,
        'email': email,
        'telefone': telefone,
        'mensagem': mensagem,
        'assunto': assunto,
    }

    mensagem = get_template('landpage/contato/email.html').render(context)

    email = EmailMessage(assunto, mensagem, from_email=settings.EMAIL_HOST_USER, to=[settings.EMAIL_ADMINISTRACAO],
                         reply_to=[email])
    email.content_subtype = 'html'
    if not email.send():
        return False
    else:
        return True
