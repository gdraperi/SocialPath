from django import forms

from social.models import Users

class PostForm(forms.ModelForm):

    class Meta:
        model = Users
        fields = ('name',)