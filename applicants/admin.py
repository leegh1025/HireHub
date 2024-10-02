from django.contrib import admin
from .models import Application, ApplicationTemplate, ApplicationQuestion, Answer, Possible_date_list
from template.models import EvaluationTemplate, InterviewTemplate, InterviewQuestion

# Register your models here.

admin.site.register(Application)
admin.site.register(ApplicationTemplate)
admin.site.register(ApplicationQuestion)
admin.site.register(EvaluationTemplate)
admin.site.register(InterviewTemplate)
admin.site.register(InterviewQuestion)
admin.site.register(Answer)
admin.site.register(Possible_date_list)