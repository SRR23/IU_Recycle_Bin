from django import forms
from .models import Contact # Import your model

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

    def clean_message(self):
        data = self.cleaned_data['message']
        # Add any custom message validation here (optional)
        return data

    def save(self, commit=True):  # Override save() if using the model
        instance = Contact(  # Create a model instance
            name=self.cleaned_data['name'],
            email=self.cleaned_data['email'],
            message=self.cleaned_data['message'],
        )
        if commit:
            instance.save()
        return instance