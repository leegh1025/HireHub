from django.db.models import Q, Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from applicants.models import Application
from django.core.exceptions import PermissionDenied
from django.db import models, transaction
from django.forms import modelformset_factory
from django.views.decorators.csrf import csrf_exempt
from datetime import time
from .tasks import process_application
from django.db import transaction
from django.db.models.functions import Coalesce

from .models import Application, Answer, Possible_date_list, Comment, individualQuestion, individualAnswer, Interviewer, AudioRecording
from accounts.models import Interviewer, InterviewTeam
from template.models import ApplicationTemplate, ApplicationQuestion, InterviewTemplate, InterviewQuestion
from .forms import ApplicationForm, CommentForm, QuestionForm, AnswerForm, ApplyForm

def interview(request):
    if request.user.is_authenticated:
        applicants = Application.objects.all()
        ctx = {"applicants": applicants}
        return render(request, "applicant/interview.html", ctx)
    else:
        return redirect("accounts:login")

def change_status(request, status_zone_id, applicant_id):
    if request.method == 'POST':
        try:
            applicant = Application.objects.get(id=applicant_id)
            if status_zone_id == '1':
                applicant.status = 'interview_scheduled'
            elif status_zone_id == '2':
                applicant.status = 'interview_in_progress'
            elif status_zone_id == '3':
                applicant.status = 'interview_completed'
            applicant.save()
            return JsonResponse({'message': 'Status updated successfully'})
        except Applicant.DoesNotExist:
            return JsonResponse({'error': 'Applicant not found'}, status=404)
        except StatusZone.DoesNotExist:
            return JsonResponse({'error': 'Status zone not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)
            
def document(request):
    if request.user.is_authenticated:
        applicants = Application.objects.all()
        ctx = {"applicants": applicants}
        return render(request, "applicant/document.html", ctx)
    else:
        return redirect("accounts:login")

def search_applicant(request):
    search_txt = request.GET.get('search_txt')
    applicants = Application.objects.filter(name__icontains=search_txt)
    applicants = applicants.filter(~Q(status = 'submitted'))
    results = [{'id': applicant.id, 'name': applicant.name} for applicant in applicants]
    return JsonResponse(results, safe=False)

def pass_document(request, applicant_id):
    if request.method == 'POST':
        try:
            applicant = Application.objects.get(pk=applicant_id)
            applicant.status = 'interview_scheduled'
            applicant.save()
            return JsonResponse({'success': True})
        except Application.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Applicant not Found'})

def fail_document(request, applicant_id):
    if request.method == 'POST':
        try:
            applicant = Application.objects.get(pk=applicant_id)
            applicant.status = 'submitted'
            applicant.save()
            return JsonResponse({'success': True})
        except Application.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Applicant not Found'})
    
def delete_recording(request, pk):
    applicant = get_object_or_404(Application, pk=pk)
    if request.method == 'POST':
        try:
            application = get_object_or_404(Application, pk=pk)
            recording = get_object_or_404(AudioRecording, application=applicant)
            recording.file.delete()  # 파일 시스템에서 파일 삭제
            recording.delete()  # DB에서 레코드 삭제
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
    

def schedule(request):
    if request.user.is_authenticated:
        applicants = Application.objects.filter(~Q(status ='submitted'))
        schedules = Possible_date_list.objects.all()

        ctx = {"applicants": applicants, "schedules":schedules}
        return render(request, 'applicant/schedule.html', ctx)
    else:
        return redirect("accounts:login")
    

def auto_schedule(request):
    schedules = Possible_date_list.objects.all()

    # 스케줄 정보 리스트
    schedules_info = [[schedule.id, 0, schedule.max_possible_interview] for schedule in schedules]

    # 이미 배치된 인원 가능 인터뷰수에서 빼기
    scheduled_applicants = Application.objects.filter(interview_date__isnull=False)
    for scheduled_applicant in scheduled_applicants:
        for schedule_info in schedules_info:
            if schedule_info[0] == scheduled_applicant.interview_date.id:
                schedule_info[2] -= 1

    # 배치 가능 인터뷰 수 0 이하면 해당 스케줄 삭제
    for schedule_info in schedules_info:
        if schedule_info[2] <=0:
            schedules_info.remove(schedule_info)

    # 지원자 정보 리스트
    applicants = Application.objects.filter(interview_date__isnull=True)
    applicants_info = [[applicant.id, list(applicant.possible_date.all())] for applicant in applicants]

    # 스케줄 짜기 알고리즘
    while schedules_info:
        # 스케줄링 필요 인원 없으면 break
        if len(applicants) == 0:
            break

        # 삭제할 인원 인덱스 리스트
        del_applicant_index = []

        # 가능 시간대 0개 or 1개 인원 배치, 인기도 갱신
        for num in range(len(applicants_info)):
            # 0개
            if len(applicants_info[num][1]) == 0:
                del_applicant_index.append(num)
            # 1개
            elif len(applicants_info[num][1]) == 1:
                applicant = Application.objects.get(id=applicants_info[num][0])
                for schedule_info in schedules_info:
                    if schedule_info[0] == applicants_info[num][1][0].id:
                        if schedule_info[2] > 0:
                            applicant.interview_date = applicants_info[num][1][0]
                            applicant.save()
                            schedule_info[2] -= 1
                            break
                        else:
                            break

                del_applicant_index.append(num)
            # 인기도 갱신
            else:
                for possible_date in applicants_info[num][1]:
                    for schedule_info in schedules_info:
                        if schedule_info[0] == possible_date.id:
                            schedule_info[1] += 1
    
        # 배치 안되거나 배치한 애들 목록에서 삭제
        for index in sorted(del_applicant_index, reverse=True):
            del applicants_info[index]
        
        del_applicant_index = []    
        # 인기도 - 남는자리수 작은 시간대 추출
        popularity = 1000000
        low_pop_schedule = []
        for schedule_info in schedules_info:
            my_popularity = schedule_info[1] - schedule_info[2]
            if popularity > my_popularity:
                popularity = my_popularity
                low_pop_schedule = schedule_info

        # 인기도 - 남는자리수 낮은 시간대 배치
        for num in range(len(applicants_info)):
            for possible_date in applicants_info[num][1]:
                if possible_date.id == low_pop_schedule[0]:
                    if low_pop_schedule[2] > 0:
                        applicant = Application.objects.get(id=applicants_info[num][0])
                        applicant.interview_date = possible_date
                        applicant.save()
                        del_applicant_index.append(num)
                        low_pop_schedule[2] -=1
                    applicants_info[num][1].remove(possible_date)

        # 배치된 인원 및 시간대 삭제
        for index in sorted(del_applicant_index, reverse=True):
            del applicants_info[index]
        del_applicant_index = []

        schedules_info.remove(low_pop_schedule)
                    
    return redirect('applicants:schedule')
    

def schedule_update(request, pk):
    applicant = get_object_or_404(Application, id=pk)

    if request.method == 'POST':
        date_id = request.POST.get('selectDate')
        time_value = request.POST.get('selectTime')

        possible_date = get_object_or_404(Possible_date_list, id=date_id)
        
        # Parsing the time value from string to time object
        print(time_value[0])
        interview_time = f'{time_value[0]}{time_value[1]}:{time_value[3]}{time_value[4]}'
        if time_value[0] == '-':
            applicant.interview_time = None
        else:
            applicant.interview_time = interview_time
        applicant.interview_date = possible_date
        applicant.save()

        return redirect('applicants:schedule')

    return redirect('applicants:schedule')

def profile(request, pk):
    if request.user.is_authenticated:
        applicant = get_object_or_404(Application, pk=pk)
        answers = Answer.objects.filter(application=applicant)
        # 리코딩
        recording = AudioRecording.objects.filter(application=applicant).first()

        # 코멘트
        comments = Comment.objects.filter(application=applicant).order_by('created_at')
        form = CommentForm()

        # 질문 생성
        questions = individualQuestion.objects.filter(application=applicant).order_by('created_at')
        question_form = QuestionForm()
        answer_form = AnswerForm()

        # 공통 질문 템플릿 및 질문 가져오기
        common_template = InterviewTemplate.objects.get(is_default=True)
        common_questions = InterviewQuestion.objects.filter(template=common_template)
        
        # 녹음 파일 업로드 처리
        if request.method == 'POST' and request.FILES.get('audio_data'):
            try:
                # AudioRecording 객체 생성 또는 가져오기
                recording, created = AudioRecording.objects.get_or_create(application=applicant)
                recording.file = request.FILES['audio_data']
                recording.save()
                return JsonResponse({'file_url': recording.file.url})
            except Exception as e:
                print(f"Error saving file: {e}")
                return JsonResponse({'error': f'File upload failed: {str(e)}'}, status=500)

        ctx = {
            'applicant': applicant,
            'answers': answers,
            'recording_exists': recording is not None,
            'comments': comments,
            'form': form,
            'questions': questions,
            'question_form': question_form,
            'answer_form': answer_form,
            'common_questions': common_questions,
        }
        
        return render(request, 'applicant/profile.html', ctx)
    else:
        return redirect("accounts:login")
    

def comment(request, pk):
    applicant = get_object_or_404(Application, pk=pk)
    answers = Answer.objects.filter(application=applicant)
    comments = Comment.objects.filter(application=applicant).order_by('created_at')
    form = CommentForm()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.method == "GET":
            ctx = {
            'applicant_id':pk,
            'applicant': applicant,
            'answers': answers,
            'comments': comments,
            'form': form,
            }
            return render(request, 'applicant/comments.html', ctx)

        # POST 일때
        else:
            interviewer = get_object_or_404(Interviewer, email=request.user.email)  # 인터뷰어 객체 가져오기
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.application = applicant
                comment.interviewer = interviewer
                comment.save()
                return JsonResponse({
                    'success': True,
                    'comment': {
                        'text': comment.text,
                        'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                        'interviewer': interviewer.name,  # 인터뷰어 이메일 반환
                        'id': comment.id
                    }
                })
    return JsonResponse({'success': False, 'error': 'Invalid form submission', 'form_errors': form.errors.as_json()})
    

def delete_comment(request, pk, comment_id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            comment = Comment.objects.get(pk=comment_id, application_id=pk)
            comment.delete()
            return JsonResponse({'success': True})
        except individualQuestion.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Question does not exist.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

def question(request, pk):
    applicant = get_object_or_404(Application, pk=pk)
    answers = Answer.objects.filter(application=applicant)
    questions = individualQuestion.objects.filter(application=applicant).order_by('created_at')
    question_form = QuestionForm()
    answer_form = AnswerForm()

    # 공통 질문 템플릿 및 질문 가져오기
    common_template = InterviewTemplate.objects.get(is_default=True)
    common_questions = InterviewQuestion.objects.filter(template=common_template)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.method == "GET":
            ctx = {
                'applicant': applicant,
                'answers': answers,
                'questions': questions,
                'question_form': question_form,
                'answer_form': answer_form,
                'common_questions': common_questions,
            }
            return render(request, 'applicant/questions.html', ctx)    
        
        else:
            if 'question_submit' in request.POST:
                interviewer = get_object_or_404(Interviewer, email=request.user.email)
                question_form = QuestionForm(request.POST)
                if question_form.is_valid():
                    question = question_form.save(commit=False)
                    question.application = applicant
                    question.interviewer = interviewer
                    question.save()
                    return JsonResponse({
                        'success': True,
                        'question': {
                            'text': question.text,
                            'created_at': question.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                            'interviewer': interviewer.name,
                            'id': question.id
                        }
                    })
                else:
                    # 폼이 유효하지 않은 경우 오류 메시지 반환
                    return JsonResponse({'success': False, 'error': 'Invalid form submission', 'form_errors': question_form.errors.as_json()})
            
            elif 'answer_submit' in request.POST:
                interviewer = get_object_or_404(Interviewer, email=request.user.email)
                answer_form = AnswerForm(request.POST)
                if answer_form.is_valid():
                    answer = answer_form.save(commit=False)
                    answer.application = applicant
                    answer.interviewer = interviewer
                    answer.question_id = request.POST.get('question_id')
                    answer.save()
                    return JsonResponse({
                        'success': True,
                        'answer': {
                            'text': answer.text,
                            'created_at': answer.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                            'interviewer': interviewer.email,
                            'id': answer.id
                        }
                    })
                else:
                    # 폼이 유효하지 않은 경우 오류 메시지 반환
                    return JsonResponse({'success': False, 'error': 'Invalid form submission', 'form_errors': question_form.errors.as_json()})
            
            else:
                print("iui")
                # 폼이 유효하지 않은 경우 오류 메시지 반환
                return JsonResponse({'success': False, 'error': 'Invalid form submission', 'form_errors': question_form.errors.as_json()})
            

def delete_question(request, pk, question_id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            question = individualQuestion.objects.get(pk=question_id, application_id=pk)
            question.delete()
            return JsonResponse({'success': True})
        except individualQuestion.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Question does not exist.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

def delete_answer(request, pk, answer_id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            answer = individualAnswer.objects.get(pk=answer_id, application_id=pk)
            answer.delete()
            return JsonResponse({'success': True})
        except individualQuestion.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Question does not exist.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

def applicant_rankings(req):
    applications = Application.objects.annotate(
        total_score=Coalesce(Sum('evaluations__total_score', filter=models.Q(evaluations__is_submitted=True)),0) # Evaluation모델을 역참조
    ).order_by('-total_score')
    interview_teams = InterviewTeam.objects.all()
    for interview_team in interview_teams:
        score_list = []
        for application in applications:
            # 팀을 자동설정 해주는 로직
            if set(interview_team.members.all()) == set(application.interviewer.all()):
                application.interview_team = interview_team
                application.save()
            # 설정된 팀을 가지고 
            if interview_team == application.interview_team:
                score_list.append(application.total_score)
                
        if len(score_list) != 0:
            interview_team.average_score = round(sum(score_list)/len(score_list),2)
            interview_team.save()
    context = {
        'applications': applications,
        'interview_teams': interview_teams,
    }
    return render(req, 'applicant_rankings.html', context)

## 지원 ##
def apply(request, pk):
    template = ApplicationTemplate.objects.get(id=pk)
    form = ApplyForm()

    if request.method == 'POST':
        form = ApplyForm(request.POST)
        if form.is_valid():
            applyContent = form.save(commit=False)
            applyContent.template = template
            applyContent.save()
            form.save_m2m()

            answers = {}
            for question in template.questions.all():
                answer_text = request.POST.get(f'answer_{question.id}')
                answers[question.id] = answer_text

            
            transaction.on_commit(lambda: process_application.apply_async(args=(applyContent.id, answers), countdown=5))

            name = form.cleaned_data['name']
            phone_number = form.cleaned_data['phone_number']
            request.session['name'] = name
            request.session['phone_number'] = phone_number
            request.session['submitted'] = True

            return redirect('applicants:apply_result')
    
    context = {
        'form': form,
        'template': template,
    }
    return render(request, 'for_applicant/write_apply.html', context)

def apply_check(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        request.session['name'] = name
        request.session['phone_number'] = phone_number
        request.session['submitted'] = False
        return redirect('applicants:apply_result')
    return render(request, 'for_applicant/apply_check.html')

def apply_result(request):
    name = request.session.get('name')
    phone_number = request.session.get('phone_number')
    submitted = request.session.get('submitted')
    if name and phone_number:
        if submitted == False:
            try:
                application = Application.objects.get(name=name, phone_number=phone_number)
                submitted = True
            except Application.DoesNotExist:
                submitted = False
        context = {
            'submitted': submitted,
        }
        return render(request, 'for_applicant/apply_result.html', context)
    else:
        return redirect('applicants:apply_check')

def apply_timeover(request):
    return render(request, 'for_applicant/timeover.html')