from django import forms
from FlashDS.models import Courier

class PayoutForm(forms.ModelForm):
    class Meta:
        model = Courier
        fields = ('paypal_mail',)