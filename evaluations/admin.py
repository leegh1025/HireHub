from django.contrib import admin
from .models import Evaluation, EvaluationScore

# EvaluationScore를 Evaluation의 인라인으로 설정
class EvaluationScoreInline(admin.TabularInline):
    model = EvaluationScore
    extra = 1  # 추가 폼 수

# Evaluation에 인라인 추가
@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    inlines = [EvaluationScoreInline]
    list_display = ('application', 'interviewer', 'total_score', 'is_submitted')
    search_fields = ('application__name', 'interviewer__name')
