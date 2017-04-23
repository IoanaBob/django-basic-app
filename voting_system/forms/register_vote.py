from django import forms

from voting_system.models import VoterAuth, VoterCode

# Ref: http://stackoverflow.com/questions/34609830/django-modelform-how-to-add-a-confirm-password-field

class RegisterVoteForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    password_hash=forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = VoterAuth
        fields = ('id','voter_id', 'password_hash', 'election_id')

    def clean(self):
        cleaned_data = super(RegisterVoteForm, self).clean()
        voter_id = cleaned_data.get("voter_id")
        password = cleaned_data.get("password_hash")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match."
            )

        if not VoterCode.objects.filter(voter_id = voter_id).exists():
            raise forms.ValidationError(
                "Voter ID is not valid."
            )

