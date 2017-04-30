from django import forms

from voting_system.models.election import Election
from voting_system.models.candidate import Candidate

class ElectionForm(forms.ModelForm):
	#"first past the post" and "single transferable vote"
	choices = ('fptp', 'stv')
	id = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	election_method = forms.ChoiceField(label='Election Method', choices=( ('fptp', 'First Past the Post'), ('stv','Single Transferable Vote')), widget=forms.Select(attrs={'style':'background_color:#F5F8EC;', 'class': 'js-example-basic-single'}))

	class Meta:
		model = Election
		fields = ('id', 'uninominal_voting','name', 'start_date','end_date', 'election_method' )
		widgets = {
			'start_date':  forms.DateInput(),
			'end_date':  forms.DateInput()
		 }