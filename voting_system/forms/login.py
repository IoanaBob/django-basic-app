from django import forms

from voting_system.models.login_model import LoginModel
from voting_system.models import Verify, VerifyLogin
class LoginForm(forms.ModelForm):

    class Meta:
        model = LoginModel
        fields = ('username', 'password')
        widgets = {
            'password':  forms.PasswordInput()
         }



class VerifyLoginForm(forms.ModelForm):

    class Meta:
        model = VerifyLogin
        fields = ('email', 'password')
        widgets = {
            'password':  forms.PasswordInput(),
            
         }