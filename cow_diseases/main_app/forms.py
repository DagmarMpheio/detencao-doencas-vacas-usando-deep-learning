from django.forms import ModelForm
from .models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {
                'class': 'form-control block w-full px-3 py-1.5 mb-2 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none',
                'placeholder': 'Primeiro Nome',
                'type':'text',
                'required': 'required'
            })
        self.fields['last_name'].widget.attrs.update(
            {
                'class': 'form-control block w-full px-3 py-1.5 mb-2 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none',
                'placeholder': 'Último Nome',
                'type':'text',
                'required': 'required'
            })
        self.fields['email'].widget.attrs.update(
            {
                'class': 'form-control block w-full px-3 py-1.5 mb-2 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none',
                'placeholder': 'Email',
                'type':'email',
                'required': 'required'
            })
