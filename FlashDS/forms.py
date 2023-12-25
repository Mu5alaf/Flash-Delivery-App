from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Sign_up_Form(UserCreationForm):
    email = forms.EmailField(max_length=100)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    # password1 is first password
    # password2 is the confirmation password
    # from user model a Prepared form to make it easy on you
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')
# email checker if email already exists
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email):
            raise ValidationError("This Email address already Exists")
        return email
    