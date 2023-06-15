from django import forms
from .models import SkinDiseasesClassification

class SkinDiseasesClassificationForm(forms.ModelForm):
    class Meta:
        model = SkinDiseasesClassification
        fields = ['skin_image']