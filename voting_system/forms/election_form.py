from django import forms

from voting_system.models.election import Election
from voting_system.models.candidate import Candidate

class ElectionForm(forms.ModelForm):
	id = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	class Meta:
		model = Election
		fields = ('id', 'uninominal_voting','start_date','end_date' )
		widgets = {
			'start_date':  forms.DateInput(),
			'end_date':  forms.DateInput()
		 }