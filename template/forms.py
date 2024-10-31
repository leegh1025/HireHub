from django import forms
from .models import ApplicationTemplate, ApplicationQuestion, EvaluationTemplate, EvaluationQuestion, InterviewTemplate, InterviewQuestion

class ApplicationTemplateForm(forms.ModelForm):
    class Meta:
        model = ApplicationTemplate
        fields = ['name' , 'description']

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': '템플릿 제목을 입력하세요.'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': '(선택) 지원자들을 위한 지원서 작성 가이드를 입력해 주세요.'
            }),
        }

class ApplicationQuestionForm(forms.ModelForm):
    class Meta:
        model = ApplicationQuestion
        fields = ['question_text', "allow_file_upload", "file_upload"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        if self.instance.allow_file_upload:
            self.fields['file_upload'] = forms.FileField(required=False)

class InterviewTemplateForm(forms.ModelForm):
    class Meta:
        model = InterviewTemplate
        fields = ['name' , 'description']

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': '질문지 제목을 입력하세요.'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': '(선택) 기본적인 공통 면접 질문을 작성해주세요.'
            }),
        }
class InterviewQuestionForm(forms.ModelForm):
    class Meta:
        model = InterviewQuestion
        fields = ['question_text']

class EvaluationTemplateForm(forms.ModelForm):
    class Meta:
        model = EvaluationTemplate
        fields = ['title' , 'description']

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': '평가표 제목을 입력하세요.'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': '(선택) 해당 평가표에 대한 설명글을 입력할 수 있습니다.'
            }),
        }

class EvaluationQuestionForm(forms.ModelForm):
    class Meta:
        model = EvaluationQuestion
        fields = ['question_title', 'question_text'] 


