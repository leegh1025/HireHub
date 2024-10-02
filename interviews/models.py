from django.db import models
from accounts.models import Interviewer
from applicants.models import Application
from template.models import InterviewTemplate, InterviewQuestion 

class Interview(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='interviews')
    interviewer = models.ForeignKey(Interviewer, on_delete=models.CASCADE)
    interview_date = models.DateTimeField()
    location = models.CharField(max_length=255)


class InterviewAnswer(models.Model):
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(InterviewQuestion, on_delete=models.CASCADE)
    answer_text = models.TextField()
    recorded_by = models.ForeignKey(Interviewer, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)


