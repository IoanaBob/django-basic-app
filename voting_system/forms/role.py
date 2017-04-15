from django import forms

from voting_system.models.role import Role

class RoleForm(forms.ModelForm):
	id = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	class Meta:
		model = Role
		fields = ('id', 'name',)