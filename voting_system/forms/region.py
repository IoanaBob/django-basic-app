from django import forms

from voting_system.models.region import Region

class RegionForm(forms.ModelForm):
	id = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	class Meta:
		model = Region
		fields = ('id', 'name',)