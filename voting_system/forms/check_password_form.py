from django import forms

from voting_system.models.voter_auth import VoterAuth


class CheckPasswordForm(forms.ModelForm):

    class Meta:
        model = VoterAuth
        fields = ('id', 'password_hash')