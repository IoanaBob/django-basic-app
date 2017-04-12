from django import forms

from voting_system.models.party import Party

class PartyForm(forms.ModelForm):
	id = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	class Meta:
		model = Party
		fields = ('id', 'name',)