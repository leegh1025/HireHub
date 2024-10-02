from django.urls import path
from . import views

app_name = 'template'

urlpatterns = [
    path('list/', views.TemplateListView.as_view(), name ='template_list'),
    path('apply/create',views.ApplicationTemplateCreateView.as_view(), name='apply_create'),
    path('apply/<int:pk>', views.TemplateDetailView.as_view(), name='template_detail'),
    path('apply/<int:pk>/update', views.TemplateUpdateView.as_view(), name='template_update'),
    path('apply/<int:pk>/delete', views.TemplateDeleteView.as_view(), name='template_delete'),
    path('interview/create',views.InterviewTemplateCreateView.as_view(), name='interview_create'),
    path('interview/<int:pk>', views.InterviewDetailView.as_view(), name='interview_detail'),
    path('interview/<int:pk>/update', views.InterviewUpdateView.as_view(), name='interview_update'),
    path('interview/<int:pk>/delete', views.InterviewDeleteView.as_view(), name='interview_delete'),
    path('evaluate/create', views.EvaluationTemplateCreateView.as_view(), name='evaluate_create'),
    path('evaluate/<int:pk>/detail', views.EvaluateDetailView.as_view(), name='evaluate_detail'),
    path('evaluate/<int:pk>/update', views.EvaluateUpdateView.as_view(), name='evaluate_update'),
    path('evaluate/<int:pk>/delete', views.EvaluateDeleteView.as_view(), name='evaluate_delete'),
]