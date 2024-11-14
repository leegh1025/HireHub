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
    school = forms.CharField(
        label = "대학교",
        widget=forms.TextInput(attrs={'placeholder': '피로대학교', 'class': 'apply_input'})
    )
    major = forms.CharField(
        label = "학과",
        widget=forms.TextInput(attrs={'placeholder': '피로학과, 컴퓨터공학과', 'class': 'apply_input'}),
        help_text="복수전공이나 부전공인 경우 모두 적어주세요."
    )
    major_type = forms.ChoiceField(
        choices=[
            ('major', '전공자'),
            ('non_major', '비전공자'),
            ('double_major', '복수전공자'),
        ],
        label="전공 여부",
        widget=forms.Select(attrs={'class': 'apply_input'}),
    )
    year = forms.ChoiceField(
        choices=[
            ('1', '1학년'),
            ('2', '2학년'),
            ('3', '3학년'),
            ('4', '4학년'),
            ('5', '5학년 이상'),
        ],
        label="학년 (휴학 중인 경우, 수료한 학년을 기준으로 선택해주세요.)",
        widget=forms.Select(attrs={'class': 'apply_input'}),
    )
    residence = forms.CharField(
        label="활동 기간 중 거주지",
        widget=forms.TextInput(attrs={'placeholder': '서울특별시'}),
        help_text="워크숍, 최종 프로젝트 발표와 같은 주요 행사와 일부 세션은 서울에서 대면으로 진행할 예정입니다."
    )
    phone_number = forms.CharField(
        label = "전화번호",
        widget=forms.TextInput(attrs={'placeholder': '기호 없이 번호를 입력해주세요.', 'class': 'apply_input'})
    )


    class Meta:
        model = Application
        fields = ['name', 'school', 'major', 'major_type', 'year', 'residence', 'phone_number', 'possible_date']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = individualQuestion
        fields = ['text']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = individualAnswer
        fields = ['text']