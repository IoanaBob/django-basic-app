from django import forms

from voting_system.models.test import Test
class TestForm(forms.ModelForm):

    class Meta:
        model = Test
        fields = ('ID', 'name',)