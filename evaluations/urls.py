from django.urls import path
from . import views

app_name = 'evaluations'

urlpatterns = [
    path('evaluations/create/<int:pk>', views.create_evaluation, name='evaluation_create'),
    path('evaluations/update/<int:pk>', views.update_evaluation, name='update_evaluation'),
    path('evaluations/comment/<int:application_id>', views.evaluation_comment, name='evaluation_comment'),
]