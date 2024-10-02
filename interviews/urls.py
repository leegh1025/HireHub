from django.urls import path
from . import views

app_name = 'interviews'

urlpatterns = [
    path('auto_questions/<int:application_id>/', views.generate_questions, name='generate_questions'),
]