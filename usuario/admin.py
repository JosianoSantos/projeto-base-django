from django.contrib import admin

from usuario.models import Usuario


class UsuarioAdmin(admin.ModelAdmin):
    pass
admin.site.register(Usuario, UsuarioAdmin)