from django import forms
from django.contrib.auth.models import User
from FlashDS.models import Client,Request
# user forms
class clientForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name')
# -----------------------------------------------------------
class ClientCustomForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ("picture",)
# ---------------------------------------------------------------
#Step 1
class Create_Request_form_1(forms.ModelForm):
    class Meta:
        model = Request
        fields = ('name','description','category','size','amount','picture')
#Step 2
class Create_Request_form_2(forms.ModelForm):
    pickup_address = forms.CharField(required=True)
    pickup_name = forms.CharField(required=True)
    pickup_phone = forms.CharField(required=True)
    class Meta:
        model = Request
        fields = ('pickup_address','pickup_lat','pickup_lng','pickup_phone','pickup_name')
# step 3
class Create_Request_form_3(forms.ModelForm):
    delivery_address = forms.CharField(required=True)
    delivery_name = forms.CharField(required=True)
    delivery_phone = forms.CharField(required=True)
    class Meta:
        model = Request
        fields = ('delivery_address','delivery_name','delivery_phone','delivery_lat','delivery_lng')