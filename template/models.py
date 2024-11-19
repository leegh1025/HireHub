from django.db import models
from accounts.models import Interviewer
# Create your models here.
class ApplicationTemplate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(Interviewer, on_delete=models.CASCADE)
    is_default = models.BooleanField(default=False, verbose_name="기본 템플릿으로 설정")


    def __str__(self):
        return self.name

# 여기서 질문을 추가할 수 있게 해놓음
class ApplicationQuestion(models.Model):
    template = models.ForeignKey(ApplicationTemplate, on_delete=models.CASCADE, related_name='questions') # related_name쓰면 접근시 easy해서 쓴겨
    question_text = models.TextField()
    max_length = models.PositiveIntegerField(null=True, blank=True)
    allow_file_upload = models.BooleanField(default = False) 
    file_upload = models.FileField(upload_to='uploads/', blank=True, null=True) #파일 업로드 필드

    def __str__(self):
        return self.question_text

class InterviewTemplate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(Interviewer, on_delete=models.CASCADE)
    is_default = models.BooleanField(default=False, verbose_name="기본 템플릿으로 설정")

    def __str__(self):
        return self.name

class InterviewQuestion(models.Model):
    template = models.ForeignKey(InterviewTemplate, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()

    def __str__(self):
        return self.question_text

class EvaluationTemplate(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(Interviewer, on_delete=models.CASCADE)
    is_default = models.BooleanField(default=False, verbose_name="기본 템플릿으로 설정")

    
    def __str__(self):
        return self.title

class EvaluationQuestion(models.Model):
    template = models.ForeignKey(EvaluationTemplate, on_delete=models.CASCADE, related_name='questions')
    question_title = models.CharField(max_length=200)
    question_text = models.TextField()

    def __str__(self):
        return self.question_title
