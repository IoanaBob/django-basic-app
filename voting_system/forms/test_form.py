from django import forms

from voting_system.models.test import Test
from voting_system.models.election import Election

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