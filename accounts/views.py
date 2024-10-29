from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.urls import reverse
from applicants.models import Application
from .forms import SignupForm, LoginForm
from django.contrib import messages
from .models import Interviewer

# Create your views here.

def landing(request):
   if request.user.is_authenticated: # 만약 사용자가 로그인되어 있다면 바로 메인 페이지로 가도록
      if isinstance(request.user, Interviewer):
         return redirect(reverse('accounts:mainboard', kwargs={'pk': request.user.pk}))
   return render(request, 'accounts/landing.html')

# 면접관 초기 페이지
def initialInterviewer(request):
   if request.user.is_authenticated: # 만약 사용자가 로그인되어 있다면 바로 메인 페이지로 가도록
      if isinstance(request.user, Interviewer):
         return redirect(reverse('accounts:mainboard', kwargs={'pk': request.user.pk}))
   return render(request, 'accounts/initial.html')

def signup(request):
   if request.method == 'GET':
      form = SignupForm()
      context = {'form': form}
      return render(request, 'accounts/signup.html', context)
   else:
      form = SignupForm(request.POST)
      if form.is_valid():
         interviewer = form.save(commit=False)
         interviewer.is_approved = False # 관리자의 승인이 필요하므로 비활성화
         interviewer.save()
         messages.success(request, '회원가입이 완료되었습니다. 관리자의 승인을 기다려주세요!')
         return redirect('accounts:initialInterviewer')
      else:
         context = {'form': form}
         return render(request, 'accounts/signup.html', context)

def login(request):
   if request.method == 'POST':
      form = LoginForm(request, request.POST)
      if form.is_valid():
         email = form.cleaned_data.get('username')
         password = form.cleaned_data.get('password')
         user = authenticate(request, username=email, password=password)
         if user is not None:
            if user.is_approved and user.is_active: # 관리자의 승인을 받았으며 활성화되었을 때
               auth_login(request, user)
               return redirect(reverse('accounts:mainboard', kwargs={'pk': user.pk})) # 로그인한 유저의 mainboard로 이동
            else:
               messages.info(request, '관리자의 승인이 필요하거나 계정이 비활성화되었습니다. 관리자에게 문의해주세요!')
               return redirect('accounts:initialInterviewer')
         else:
            form.add_error(None, '이메일 또는 비밀번호가 잘못되었습니다.')
   else:
      form = LoginForm()

   context = {'form': form}
   return render(request, 'accounts/login.html', context)

def logout(request):
   auth_logout(request)
   return redirect('accounts:initialInterviewer')

def mainboard(request,pk):
   if request.user.is_authenticated:
      if isinstance(request.user, Interviewer):
         applicants = Application.objects.filter(interviewer=pk)
         sort_applicants = Application.objects.filter(interviewer=pk)
         sort = request.GET.get('sort','')

         if sort == 'submitted':
            sort_applicants = sort_applicants.filter(status='submitted')
         elif sort == 'scheduled':
            sort_applicants = sort_applicants.filter(status='interview_scheduled')
         elif sort == 'in_progress':
            sort_applicants = sort_applicants.filter(status='interview_in_progress')
         elif sort == 'completed':
            sort_applicants = sort_applicants.filter(status='interview_completed')
         else:
            sort_applicants = sort_applicants

         interview_num = applicants.filter(~Q(status='submitted')).count()
         ctx = {"applicants":applicants, "sort_applicants":sort_applicants, "pk":pk, "interview_num": interview_num}
         return render(request, "mainboard.html", ctx)
   else:
      return redirect("accounts:login")
