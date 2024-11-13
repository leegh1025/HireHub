from django import forms
from .models import ApplicationTemplate, ApplicationQuestion, Comment, individualQuestion, individualAnswer
from .models import ApplicationTemplate, Comment, Application, Possible_date_list
from .models import Applicant
from django.contrib.auth.forms import PasswordResetForm

# '이메일 유효성 검사' 추가된 PasswordResetForm
class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not Applicant.objects.filter(email=email).exists():
            raise forms.ValidationError("해당 이메일은 가입되어 있지 않습니다.")
        return email


class ApplicationForm(forms.ModelForm):
    name = forms.CharField(label='Name', max_length=100)

    class Meta:
        model = ApplicationTemplate
        fields = ['name','description']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class ApplyForm(forms.ModelForm):
    possible_date = forms.ModelMultipleChoiceField(
        queryset = Possible_date_list.objects.all(),
        label = "면접 가능한 시간대를 모두 선택해주세요",
        widget = forms.CheckboxSelectMultiple(attrs={'class': 'apply_input'}),
    )
    name = forms.CharField(
        label = "이름",
        widget=forms.TextInput(attrs={'class': 'apply_input'}),
    )
    phone_number = forms.CharField(
        label = "전화번호",
        widget=forms.TextInput(attrs={'placeholder': '기호 없이 번호를 입력해주세요.', 'class': 'apply_input'})
    )
    school = forms.CharField(
        label = "대학교",
        widget=forms.TextInput(attrs={'placeholder': '피로대학교', 'class': 'apply_input'})
    )
    major = forms.CharField(
        label = "학과",
        widget=forms.TextInput(attrs={'placeholder': '주전공 (예: 피로학과)', 'class': 'apply_input'})
    )
    class Meta:
        model = Application
        fields = ['name', 'phone_number', 'school', 'major', 'possible_date']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = individualQuestion
        fields = ['text']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = individualAnswer
        fields = ['text']