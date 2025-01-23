from django import forms
from .models import OfferApplication , Offer

class OfferApplicationForm(forms.ModelForm):
    class Meta:
        model = OfferApplication
        fields = ['full_name', 'email','description']

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['title','description','supervisor','skills_required','duration','is_active']