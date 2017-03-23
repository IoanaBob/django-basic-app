from django import forms

from voting_system.models.candidate import Candidate
from voting_system.models.party import Party

class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.name
class CandidateForm(forms.ModelForm):

	id = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	partyData = Party.objects.only('id', 'name')
	
	party_id = UserModelChoiceField(required=True, queryset=(partyData), widget=forms.Select(attrs={'style':'background_color:#F5F8EC'}))



	class Meta:
		model = Candidate
		fields = ('id', 'first_name', 'last_name', 'email', 'party_id')