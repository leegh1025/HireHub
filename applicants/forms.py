from django import forms
from .models import ApplicationTemplate, ApplicationQuestion, Comment, individualQuestion, individualAnswer
from .models import ApplicationTemplate, Comment, Application, Possible_date_list
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Applicant

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
        widget=forms.TextInput(attrs={'placeholder': '이름 (예: 홍길동)', 'class': 'apply_input'})
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '전화번호 (예: 01012345678)', 'class': 'apply_input'})
    )
    school = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '대학교 (예: 피로대학교)', 'class': 'apply_input'})
    )
    major = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '주전공 (예: 피로학과)', 'class': 'apply_input'})
    )
    class Meta:
        model = Application
        fields = ['name', 'phone_number', 'school', 'major', 'possible_date']
    
    def __init__(self, *args, **kwargs):
        super(ApplyForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = ''
        self.fields['phone_number'].label = ''
        self.fields['school'].label = ''
        self.fields['major'].label = ''

class QuestionForm(forms.ModelForm):
    class Meta:
        model = individualQuestion
        fields = ['text']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = individualAnswer
        fields = ['text']