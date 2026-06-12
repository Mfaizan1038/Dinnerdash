from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=150,required=True)
    display_name = forms.CharField(max_length=32,min_length=2,required=False)

    class Meta:
        model = User
        fields = ('email','full_name', 'display_name','password1','password2')
        
        def clean_email(self):
            email = self.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('User exists with this email')
            return email
        
        def save(self, commit=True):
            user = super().save(commit=False)
            user.email = self.cleaned_data['email']
            user.full_name = self.cleaned_data['full_name']
            user.display_name = self.cleaned_data['display_name']
            user.username = user.email
            if commit :
                user.save()
            return user
class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email')

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('full_name', 'display_name')