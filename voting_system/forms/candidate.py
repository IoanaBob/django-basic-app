from django import forms
from django.utils.translation import ugettext_lazy as _
from voting_system.models.region import Region
from voting_system.models.candidate import Candidate
from voting_system.models.party import Party

class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.name
class CandidateForm(forms.ModelForm):

	id = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	party_id = UserModelChoiceField(required=True, label="Party", queryset=(Party.objects.only('id', 'name')), widget=forms.Select(attrs={'style':'background_color:#F5F8EC; float: right', 'class': 'js-example-basic-single'}))
	region_id = UserModelChoiceField(required=True, label="Region", queryset=(Region.objects.only('id', 'name')), widget=forms.Select(attrs={'style':'background_color:#F5F8EC; float: right', 'class': 'js-example-basic-single region_dropdown'}))

	class Meta:
		model = Candidate
		fields = ('id', 'first_name', 'last_name', 'email', 'party_id', 'region_id')
		labels = {
			'first_name': _('First Name'),
			'last_name': 'Last Name',
			}