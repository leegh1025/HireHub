from django.db import models
from accounts.models import Interviewer
from applicants.models import Application
from template.models import EvaluationTemplate, EvaluationQuestion
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.
class Evaluation(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='evaluations')
    interviewer = models.ForeignKey(Interviewer, on_delete=models.CASCADE)
    template = models.ForeignKey(EvaluationTemplate, on_delete=models.CASCADE, default=1)
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_score = models.IntegerField(default=0)
    is_submitted = models.BooleanField(default=False)  # 평가 제출 여부

    def calculate_total_score(self):
        total = self.scores.aggregate(total=models.Sum('score'))['total'] or 0
        self.total_score = total
        self.save()

class EvaluationScore(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='scores')
    question = models.ForeignKey(EvaluationQuestion, on_delete=models.CASCADE)
    score = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])