from django import forms

from usuario.models import Usuario


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'tipo', 'email', 'password', 'is_active']

    password = forms.CharField(label='Senha', widget=forms.PasswordInput, max_length=50)


class UsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'tipo', 'email', 'is_active']
