from django.forms import ModelForm
from .models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email','telefone','data_nascimento','genero','endereco','bio']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {
                'class': 'form-control',
                'placeholder': 'Primeiro Nome',
                'type':'text',
                'required': 'required'
            })
        self.fields['last_name'].widget.attrs.update(
            {
                'class': 'form-control',
                'placeholder': 'Último Nome',
                'type':'text',
                'required': 'required'
            })
        self.fields['email'].widget.attrs.update(
            {
                'class': 'form-control',
                'placeholder': 'Email',
                'type':'email',
                'required': 'required'
            })
        self.fields['telefone'].widget.attrs.update(
            {
                'class': 'form-control',
                'placeholder': 'Telefone',
                'type':'tel',
            })
        self.fields['data_nascimento'].widget.attrs.update(
            {
                'class': 'form-control',
                'placeholder': 'Data de Nascimento',
                'type':'date',
            })
        self.fields['genero'].widget.attrs.update(
            {
                'class': 'form-control',
                'placeholder': 'Gênero',
                'type':'radio',
            })
        """ self.fields['fb_link'].widget.attrs.update(
            {
                'class': 'form-control',
                'type':'url',
            })
        self.fields['twitter_link'].widget.attrs.update(
            {
                'class': 'form-control',
                'type':'url',
            })
        self.fields['tiktok_link'].widget.attrs.update(
            {
                'class': 'form-control',
                'type':'url',
            })
        self.fields['instagram_link'].widget.attrs.update(
            {
                'class': 'form-control',
                'type':'url',
            }) """
        self.fields['endereco'].widget.attrs.update(
            {
                'class': 'form-control',
                'placeholder': 'Endereço',
                'type':'text',
            })
        self.fields['bio'].widget.attrs.update(
            {
                'class': 'form-control',
                'placeholder': 'Biografia',
                'type':'text',
            })
