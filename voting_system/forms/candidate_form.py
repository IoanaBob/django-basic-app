from django import forms

from voting_system.models.candidate import Candidate
from voting_system.models.party import Party

class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.name
class CandidateForm(forms.ModelForm):

	id = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	party_id = UserModelChoiceField(required=True, queryset=(Party.objects.only('id', 'name')), widget=forms.Select(attrs={'style':'background_color:#F5F8EC', 'class': 'js-example-basic-single'}))

	class Meta:
		model = Candidate
		fields = ('id', 'first_name', 'last_name', 'email', 'party_id')