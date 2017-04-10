from django import forms

from voting_system.models.login_model import LoginModel

class LoginForm(forms.ModelForm):

    class Meta:
        model = LoginModel
        fields = ('username', 'password')
        widgets = {
            'password':  forms.PasswordInput()
         }