from django import forms

from voting_system.models.election import Election


class ElectionForm(forms.ModelForm):

    class Meta:
        model = Election
        fields = ('id', 'name', 'uninominal_voting', 'start_date', 'end_date')
        widgets = {
            'start_date':  forms.DateInput(),
            'end_date':  forms.DateInput()
         }