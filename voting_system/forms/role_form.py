from django import forms

from voting_system.models.role import Role

class RoleForm(forms.ModelForm):

    class Meta:
        model = Role
        fields = ('id', 'name',)