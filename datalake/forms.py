from django import forms
from .models import Entity, Intent

class EntityForm(forms.ModelForm):
    class Meta:
        model = Entity
        fields = ['subject', 'entry']
        labels = {
            'subject': '엔티티명',
            'entry': '대표어',
        }
        
class IntentForm(forms.ModelForm):
    class Meta:
        model = Intent
        fields = ['subject']
        labels = {
            'subject': '인텐트명',
        }