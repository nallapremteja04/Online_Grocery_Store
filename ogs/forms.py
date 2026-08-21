from django import forms

class OCRUploadForm(forms.Form):

    image = forms.ImageField()