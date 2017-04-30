from django import forms

from voting_system.models.election import Election
from voting_system.models.candidate import Candidate
from voting_system.models.region import Region
class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.name
class ElectionForm(forms.ModelForm):
	#"first past the post" and "single transferable vote"
	choices = [('fptp','First Past the Post'),('stv','Single Transferable Vote')]
	id = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	election_method = forms.ChoiceField(label='Election Method', choices=( ('fptp', 'First Past the Post'), ('stv','Single Transferable Vote')), widget=forms.Select(attrs={'style':'background_color:#F5F8EC;', 'class': 'js-example-basic-single'}))
	region_id = UserModelChoiceField(required=True, label="Regions",empty_label=None, queryset=(Region.objects.only('id', 'name')), widget=forms.Select(attrs={'name':'regions[]', 'style':'background_color:#F5F8EC; ', 'multiple':'multiple', 'class': 'js-example-basic-multiple'}))
	class Meta:
		model = Election
		fields = ('id', 'uninominal_voting','name', 'start_date','end_date', 'election_method', 'region_id' )
		widgets = {
			'start_date':  forms.DateInput(),
			'end_date':  forms.DateInput()
		 }