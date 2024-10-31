from django.contrib import admin
from .models import Applicant, Application, ApplicationTemplate, ApplicationQuestion, Answer, Possible_date_list
from template.models import EvaluationTemplate, InterviewTemplate, InterviewQuestion

# Register your models here.

admin.site.register(ApplicationTemplate)
admin.site.register(ApplicationQuestion)
admin.site.register(EvaluationTemplate)
admin.site.register(InterviewTemplate)
admin.site.register(InterviewQuestion)
admin.site.register(Answer)
admin.site.register(Possible_date_list)
admin.site.register(Applicant)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'applicant', 'template', 'status', 'is_drafted', 'submission_date')
    list_filter = ('is_drafted', 'status')  # 임시저장 여부와 상태 필터 추가
    search_fields = ('applicant__username', 'name', 'template__name')