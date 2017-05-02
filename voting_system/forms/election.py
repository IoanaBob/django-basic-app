from django import forms
from django.utils.translation import ugettext_lazy as _
from voting_system.models.election import Election
from voting_system.models.candidate import Candidate
from voting_system.models.region import Region
class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.name
class ElectionForm(forms.ModelForm):
	#"first past the post" and "single transferable vote"
	
	id = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	election_method = forms.ChoiceField(label='Election Method', choices=( ('fptp', 'First Past the Post'), ('stv','Single Transferable Vote')), widget=forms.Select(attrs={'style':'background_color:#F5F8EC;', 'class': 'js-example-basic-single'}))
	regions_type = forms.ChoiceField(label='Regions Type', choices=( ('admin_district', 'Admin District'), ('parliamentary_constituency','Parliamentary Constituency'), ('european_electoral_region','European Electoral Region'),('admin_ward','Admin Ward')), widget=forms.Select(attrs={'style':'background_color:#F5F8EC;', 'class': 'js-example-basic-single'}))
	region_id = UserModelChoiceField(required=True, label="Regions",empty_label=None, queryset=(Region.objects.only('id', 'name')), widget=forms.Select(attrs={'name':'regions[]', 'style':'background_color:#F5F8EC; ', 'multiple':'multiple', 'class': 'js-example-basic-multiple'}))
	
	class Meta:
		model = Election
		fields = ('id','name', 'voting_start_date','voting_end_date','registration_start_date','registration_end_date', 'election_method',  'region_id' ,'regions_type' )
		widgets = {
			'voting_start_date':  forms.DateTimeInput(),
			'voting_end_date':  forms.DateTimeInput(),
			'registration_start_date': forms.DateTimeInput(),
			'registration_end_date': forms.DateTimeInput(),
			
		 }
		labels = {
			 "voting_start_date": _("Voting Start Date"),
			 "voting_end_date": _("Voting End Date"),
			 "registration_start_date": _("Registration Start Date"),
			 "registration_end_date": _("Registration End Date"),
		 }