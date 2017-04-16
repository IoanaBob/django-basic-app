from django import forms

from voting_system.models.admin import Admin

class AdminForm(forms.ModelForm):

	id = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	class Meta:
		model = Admin
		fields = ('id', 'first_name', 'last_name','user_name', 'email')