from django.db import models
from accounts.models import Interviewer, InterviewTeam
from template.models import ApplicationTemplate, ApplicationQuestion, EvaluationTemplate
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import datetime as dt
from django.utils import timezone
from datetime import timedelta

class Possible_date_list(models.Model):
    AMPM_CHOICES = [
        ('am', '오전'),
        ('pm', '오후'),
    ]
    # 면접일
    possible_date= models.DateField(blank=False, null=False)
    # 오전, 오후
    possible_ampm = models.CharField(max_length=50, choices=AMPM_CHOICES, blank=False, null=False)
    # 해당 타임(면접일/오전or오후) 최대 할당가능 면접 개수4
    max_possible_interview = models.IntegerField("면접타임개수", default=0)
    
    def __str__(self):
        return f'{self.possible_date}, {self.possible_ampm}'

class ApplicantManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        phone_number = extra_fields.get('phone_number')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
class Applicant(AbstractBaseUser):
    name = models.CharField(max_length=20, null=False)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=255, unique=True, null=False, blank=False)
    is_active = models.BooleanField(default=True) # 이메일 인증 전에는 비활성화
    is_staff = models.BooleanField(default=True)

    objects = ApplicantManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

class VerificationCode(models.Model):
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        expiration_time = self.created_at + timedelta(minutes=10)  # 10분 후 만료
        return timezone.now() > expiration_time

    def __str__(self):
        return f"{self.email}: {self.code}"

class Application(models.Model):
    STATUS_CHOICES = [
        ('submitted', '서류 제출'),
        ('interview_scheduled', '면접 대기'),
        ('interview_in_progress', '면접 진행 중'),
        ('interview_completed', '면접 완료'),
    ]
    TIME_CHOICES = [(None, '------')]

    for x in range(9, 18):
        TIME_CHOICES.append((dt.time(hour=x), '{:02d}:00'.format(x)))
        TIME_CHOICES.append((dt.time(hour=x, minute=30), '{:02d}:30'.format(x)))

    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    template = models.ForeignKey(ApplicationTemplate, on_delete=models.CASCADE, null=True, blank=True)
    evaluation_template = models.ForeignKey(EvaluationTemplate, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    school = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    submission_date = models.DateTimeField(auto_now_add=True)
    interviewer = models.ManyToManyField(
        Interviewer,
        limit_choices_to={'is_approved': True, 'is_active': True}
    )
    interview_team = models.ForeignKey(InterviewTeam, on_delete=models.CASCADE, blank=True, null=True, related_name='interview_team')
    possible_date = models.ManyToManyField(Possible_date_list, blank=True)
    interview_date = models.ForeignKey(Possible_date_list, on_delete=models.SET_NULL, blank=True, null=True, related_name='interview_date')
    interview_time = models.TimeField(choices=TIME_CHOICES, blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='submitted')
    is_drafted = models.BooleanField(default=True) #True면 임시저장이고, False면 최종 제출된 상태

    def __str__(self):
        return f'{self.name}'
    
    def get_total_score(self):
        return self.evaluations.filter(is_submitted=True).aggregate(total=models.Sum('total_score'))['total'] or 0

class Answer(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(ApplicationQuestion, on_delete=models.CASCADE) #특정 질문에 대한 답변
    answer_text = models.TextField(blank=True, null=True)
    file_upload = models.FileField(upload_to="uploads/", blank=True, null=True)

class Comment(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='comments')
    interviewer = models.ForeignKey(Interviewer, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.interviewer} on {self.created_at}'
    
class individualQuestion(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='individual_questions')
    interviewer = models.ForeignKey(Interviewer, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'question by {self.interviewer} on {self.created_at}'

class individualAnswer(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='individual_answers')
    question = models.ForeignKey(individualQuestion, on_delete=models.CASCADE, related_name='answers')
    interviewer = models.ForeignKey(Interviewer, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'answer by {self.interviewer} on {self.created_at}'


class AudioRecording(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='recording')
    file = models.FileField(upload_to='recordings/', blank=True, null=True)

    def __str__(self):
        return f"{self.application.name}'s Recording"