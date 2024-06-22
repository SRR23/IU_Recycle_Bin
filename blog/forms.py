
from django import forms


class TextForm(forms.Form):
    # html textarea named is message
    message = forms.CharField(widget=forms.Textarea, required=True)