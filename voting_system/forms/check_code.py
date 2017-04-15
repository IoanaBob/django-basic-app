from django import forms

from voting_system.models.voter_code import VoterCode


class CheckCodeForm(forms.ModelForm):

    class Meta:
        model = VoterCode
        fields = ('id','code')