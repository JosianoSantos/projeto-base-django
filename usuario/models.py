from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.db import models
from django.urls import reverse
from fcm_django.models import FCMDevice

from area_administracao.cliente.models import Cliente
from utils.gerador_hash import gerar_hash


class UsuarioAdministradoresAtivosManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(tipo='ADMINISTRADOR', is_active=True)


class UsuarioClientesAtivosManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(tipo='CLIENTE', is_active=True)


class Usuario(AbstractBaseUser):
    TIPOS = (
        ('ADMINISTRADOR', 'Administrador'),
        ('CLIENTE', 'Cliente'),
    )

    USERNAME_FIELD = 'email'

    tipo = models.CharField('Tipo do usuário', max_length=15, choices=TIPOS)
    nome = models.CharField('Nome', max_length=100)
    email = models.EmailField('Email', unique=True, max_length=100, db_index=True)
    is_staff = models.BooleanField('Permitir acesso como gerenciador do sistema', default=False)
    is_active = models.BooleanField('ativo', default=True, help_text='Liberar acesso ao sistema')
    clientes = models.ManyToManyField('cliente.Cliente')
    slug = models.SlugField('slug', max_length=100, null=True, blank=True)

    objects = UserManager()
    administradores_ativos = UsuarioAdministradoresAtivosManager()
    clientes_ativos = UsuarioClientesAtivosManager()

    class Meta:
        ordering = ['nome']
        verbose_name = 'usuário'
        verbose_name_plural = 'usuários'

    @property
    def get_absolute_url(self):
        return reverse('configuracao:usuario_update', kwargs={'slug': self.slug})

    @property
    def get_cliente_absolute_url(self):
        return reverse('cliente:usuario_update', kwargs={'slug': self.slug})

    @property
    def get_cliente_delete_url(self):
        return reverse('cliente:usuario_delete', kwargs={'slug': self.slug})

    @property
    def dispositivos_FCM(self):
        return FCMDevice.objects.filter(user=self)

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if self.tipo == 'ADMINISTRADOR':
            self.is_staff = True
        else:
            self.is_staff = False
        if not self.slug:
            self.slug = gerar_hash()
        super(Usuario, self).save(*args, **kwargs)
