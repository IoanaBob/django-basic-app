from django import forms

from voting_system.models.party import Party

class PartyForm(forms.ModelForm):

    class Meta:
        model = Party
        fields = ('id', 'name',)