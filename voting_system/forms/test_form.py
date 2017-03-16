from django import forms

from voting_system.models.test import Test
from voting_system.models.election import Election
from voting_system.models import VoterCode

class TestForm(forms.ModelForm):

    class Meta:
        model = Test
        fields = ('ID', 'name',)


class ElectionForm(forms.ModelForm):

    class Meta:
        model = Election
        fields = ('id', 'uninominal_voting','start_date','end_date')
        widgets = {
            'start_date':  forms.DateInput(),
            'end_date':  forms.DateInput()
         }

class VoterCodeForm(forms.ModelForm):
    election = forms.ModelChoiceField(queryset=Election.objects.all(), empty_label="Select an election")
    class Meta:
        model = VoterCode
        fields = ('election',)