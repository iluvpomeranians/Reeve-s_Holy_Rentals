from django import forms
from .models import User

class UserRegistrationForm(forms.ModelForm):
  class Meta:
    model = Userfields = ['firstName', 'lastName', 'email', 'password']
    
  def clean_email(self):
    email = self.cleaned_data['email']
    if User.objects.filter(email=email).exists():
      raise forms.ValidationError("This email is already in use.")
    return email
  
