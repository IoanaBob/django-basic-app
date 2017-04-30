from django import forms

from voting_system.models.election import Election
from voting_system.models.candidate import Candidate

class ElectionForm(forms.ModelForm):
	#"first past the post" and "single transferable vote"
	choices = [('fptp','First Past the Post'),('stv','Single Transferable Vote')]
	id = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	election_type = forms.ChoiceField(choices = choices, required=True)

	class Meta:
		model = Election
		fields = ('id', 'uninominal_voting','name', 'start_date','end_date', 'election_type' )
		widgets = {
			'start_date':  forms.DateInput(),
			'end_date':  forms.DateInput()
		 }