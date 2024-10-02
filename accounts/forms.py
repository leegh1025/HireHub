from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Interviewer

class SignupForm(UserCreationForm):
   name = forms.CharField(
      widget=forms.TextInput(attrs={'placeholder': '이름', 'class': 'signup_input'})
   )
   email = forms.EmailField(
      widget=forms.EmailInput(attrs={'placeholder': '이메일', 'class': 'signup_input'})
   )
   password1 = forms.CharField(
      widget=forms.PasswordInput(attrs={'placeholder': '비밀번호', 'class': 'signup_input'})
   )
   password2 = forms.CharField(
      widget=forms.PasswordInput(attrs={'placeholder': '비밀번호 확인', 'class': 'signup_input'})
   )

   class Meta:
      model = Interviewer
      fields = [
         "name",
         "email",
         "password1",
         "password2",
      ]
   
   def __init__(self, *args, **kwargs):
      super(SignupForm, self).__init__(*args, **kwargs)
      for field_name, field in self.fields.items():
            field.label = ''

   def clean_email(self):
      email = self.cleaned_data.get('email')
      if Interviewer.objects.filter(email=email).exists():
         raise forms.ValidationError('이 이메일은 이미 사용 중입니다')
      return email

class LoginForm(AuthenticationForm):
   username = forms.EmailField(
      widget=forms.EmailInput(attrs={'placeholder': '이메일', 'class': 'login_input'})
   )
   password = forms.CharField(
      widget=forms.PasswordInput(attrs={'placeholder': '비밀번호', 'class': 'login_input'})
   )

   def __init__(self, *args, **kwargs):
      super(LoginForm, self).__init__(*args, **kwargs)
      self.fields['username'].label = ''
      self.fields['password'].label = ''