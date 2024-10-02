from django.shortcuts import render, redirect
from .models import Evaluation, EvaluationScore
from template.models import EvaluationTemplate, EvaluationQuestion
from applicants.models import Application
from accounts.models import Interviewer
from django.http import HttpResponseForbidden
# Create your views here.

def create_evaluation(req, pk):
    if req.user.is_authenticated:
        application = Application.objects.get(id=pk)
        interviewer = Interviewer.objects.get(id = req.user.id)
        template = EvaluationTemplate.objects.get(is_default=True)

        if not interviewer in application.interviewer.all():  # 배정된 면접관인지 확인
            return HttpResponseForbidden("배정된 면접관이 아닙니다.")
        
        existing_evaluation = Evaluation.objects.filter(application=application, interviewer=interviewer, template=template, is_submitted=True).first()
        if existing_evaluation:
            return redirect ('evaluations:update_evaluation', existing_evaluation.id)

        if req.method == 'POST':
            evaluation = Evaluation.objects.create(
                application=application,
                interviewer=interviewer,
                template=template,
                comments=req.POST.get('comments', '')
            )

            for question in template.questions.all():
                score = req.POST.get(f'score_{question.id}')
                EvaluationScore.objects.create(
                    evaluation=evaluation,
                    question=question,
                    score=score
                )
                
            evaluation.is_submitted = True
            evaluation.calculate_total_score()
            evaluation.save()

            return redirect('applicants:profile', application.id)
        
        ctx = {
            'pk': pk,
            'application': application,
            'template': template,
            'questions': template.questions.all()
        }
        return render(req, 'evaluation_create.html', ctx)
    else:
        return redirect("accounts:login")

def update_evaluation(req,pk):
    evaluation = Evaluation.objects.get(id=pk)
    application = evaluation.application
    interviewer = evaluation.interviewer
    template = EvaluationTemplate.objects.get(is_default=True)

    if req.user.id != interviewer.id:
        return HttpResponseForbidden("이 평가를 수정할 권한이 없습니다.")

    if req.method == 'POST':
        evaluation.comments = req.POST.get('comments', '')

        total_score = 0
        for question in template.questions.all():
            score = req.POST.get(f'score_{question.id}')
            if score:
                total_score += int(score)
                EvaluationScore.objects.update_or_create(
                    evaluation=evaluation,
                    question=question,
                    defaults={'score': score}
                )

        evaluation.is_submitted = True
        evaluation.total_score = total_score
        evaluation.save()

        return redirect('applicants:profile', application.id)
    
    existing_scores = {
        question.id: EvaluationScore.objects.filter(evaluation=evaluation, question=question).first().score
        for question in template.questions.all()
    }
        
    ctx = {
        'evaluation': evaluation,
        'application': application,
        'template': template,
        'questions': template.questions.all(),
        'existing_scores': existing_scores,
    }
    return render(req, 'evaluation_update.html', ctx)

def evaluation_comment(req, application_id):
    application = Application.objects.get(id=application_id)
    evaluations = Evaluation.objects.filter(application = application_id)

    ctx = {
        'application': application,
        'evaluations': evaluations,
    }
    return render(req, 'evaluation_comment.html', ctx)