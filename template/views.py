from django.shortcuts import render, redirect
from .models import ApplicationTemplate, ApplicationQuestion, EvaluationTemplate, EvaluationQuestion, InterviewTemplate, InterviewQuestion
from .forms import ApplicationTemplateForm, ApplicationQuestionForm, EvaluationTemplateForm, EvaluationQuestionForm, InterviewTemplateForm, InterviewQuestionForm
from django.forms import modelformset_factory
from django.views import View
from django.views.generic.edit import DeleteView
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy


# Create your views here.
class TemplateListView(View):
    def get(self, req):
        if req.user.is_authenticated:
            template1 = ApplicationTemplate.objects.all()
            template2 = EvaluationTemplate.objects.all()
            template3 = InterviewTemplate.objects.all()
            return render(req, 'template_list.html', {'template1': template1, 'template2': template2, 'template3': template3})
        else:
            return redirect("accounts:login")
        

    
class ApplicationTemplateCreateView(View):
        def get(self, req):
            if req.user.is_authenticated:
                template_form = ApplicationTemplateForm()
                QuestionFormSet = modelformset_factory(ApplicationQuestion, form=ApplicationQuestionForm, extra=0)
                formset = QuestionFormSet(queryset=ApplicationQuestion.objects.none())
                return render(req, 'temple/apply_create.html', {
                    'template_form' : template_form,
                    'formset' : formset
                })
            else:
                return redirect("accounts:login")
        
        def post(self, req):
            if req.user.is_authenticated:
                template_form = ApplicationTemplateForm(req.POST)
                QuestionFormSet = modelformset_factory(ApplicationQuestion, form=ApplicationQuestionForm, extra=0)
                formset = QuestionFormSet(req.POST, queryset=ApplicationQuestion.objects.none())

                if template_form.is_valid():
                    template = template_form.save(commit=False)
                    template.created_by = req.user
                    template.save()

                questions = [v for k, v in req.POST.items() if k.startswith('questions[')]
                for question_text in questions:
                    ApplicationQuestion.objects.create(template=template, question_text=question_text)
            
                if formset.is_valid():
                    formset_questions = formset.save(commit=False)
                    for question in formset_questions:
                        question.template = template
                        question.save()

                    return JsonResponse({'success': True, 'redirect': reverse('template:template_list')})
                else:
                    return JsonResponse({'success': False, 'errors': template_form.errors}, status=400)
            else:
                return redirect("accounts:login")
            
    
    
class TemplateDetailView(View):
    def get(self, req, pk):
        if req.user.is_authenticated:
            template = ApplicationTemplate.objects.get(pk=pk)
            questions = template.questions.all()
            return render(req, 'temple/template_detail.html', {'template': template, 'questions':questions})
        else:
            return redirect("accounts:login")
        
    

class TemplateUpdateView(View):
    def get(self, req, pk):
        template = ApplicationTemplate.objects.get(pk=pk)
        template_form = ApplicationTemplateForm(instance=template)
        QuestionFormSet = modelformset_factory(ApplicationQuestion, form=ApplicationQuestionForm, extra=0)
        formset = QuestionFormSet(queryset=template.questions.all())
        return render(req, 'temple/apply_update.html', {
            'template_form': template_form,
            'formset': formset,
            'template': template
        })

    def post(self, req, pk):
        template = ApplicationTemplate.objects.get(pk=pk)
        template_form = ApplicationTemplateForm(req.POST, instance=template)
        QuestionFormSet = modelformset_factory(ApplicationQuestion, form=ApplicationQuestionForm, extra=0)
        formset = QuestionFormSet(req.POST, queryset=template.questions.all())

        if template_form.is_valid() and formset.is_valid():
            template = template_form.save(commit=False)
            template.created_by = req.user
            template.save()
            formset.instance = template
            formset.save()

            # 동적으로 추가된 질문들 처리
            self._save_dynamic_questions(req, template)

            return JsonResponse({'success': True, 'redirect': reverse('template:template_detail', kwargs={'pk': template.pk})})
        else:
            return JsonResponse({'success': False, 'errors': {**template_form.errors, **formset.errors}}, status=400)

    def _save_dynamic_questions(self, req, template):
        questions = [v for k, v in req.POST.items() if k.startswith('questions[')]
        for question_text in questions:
            ApplicationQuestion.objects.create(template=template, question_text=question_text)
    

class TemplateDeleteView(DeleteView):
    model = ApplicationTemplate
    success_url = reverse_lazy('template:template_list')

    def delete(self, req, *args, **kwargs):
        response = super().delete(req, *args, **kwargs)
        if req.is_ajax():
            return JsonResponse({'success': True, 'redirect': self.success_url})
        else:
            return response

class InterviewTemplateCreateView(View):
        def get(self, req):
            if req.user.is_authenticated:
                template_form = InterviewTemplateForm()
                QuestionFormSet = modelformset_factory(InterviewQuestion, form=InterviewQuestionForm, extra=0)
                formset = QuestionFormSet(queryset=InterviewQuestion.objects.none())
                return render(req, 'temple/interview_create.html', {
                    'template_form' : template_form,
                    'formset' : formset
                })
            else:
                return redirect("accounts:login")
            
        def post(self, req):
            if req.user.is_authenticated:
                template_form = InterviewTemplateForm(req.POST)
                QuestionFormSet = modelformset_factory(InterviewQuestion, form=InterviewQuestionForm, extra=0)
                formset = QuestionFormSet(req.POST, queryset=InterviewQuestion.objects.none())

                if template_form.is_valid():
                    template = template_form.save(commit=False)
                    template.created_by = req.user
                    template.save()

                questions = [v for k, v in req.POST.items() if k.startswith('questions[')]
                for question_text in questions:
                    InterviewQuestion.objects.create(template=template, question_text=question_text)
            
                if formset.is_valid():
                    formset_questions = formset.save(commit=False)
                    for question in formset_questions:
                        question.template = template
                        question.save()

                    return JsonResponse({'success': True, 'redirect': reverse('template:template_list')})
                else:
                    return JsonResponse({'success': False, 'errors': template_form.errors}, status=400)
            else:
                return redirect("accounts:login")

class InterviewDetailView(View):
    def get(self, req, pk):
        if req.user.is_authenticated:
            template = InterviewTemplate.objects.get(pk=pk)
            questions = template.questions.all()
            return render(req, 'temple/interview_detail.html', {'template': template, 'questions':questions})
        else:
            return redirect("accounts:login")

class InterviewUpdateView(View):
    def get(self, req, pk):
        template = InterviewTemplate.objects.get(pk=pk)
        template_form = InterviewTemplateForm(instance=template)
        QuestionFormSet = modelformset_factory(InterviewQuestion, form=InterviewQuestionForm, extra=0)
        formset = QuestionFormSet(queryset=template.questions.all())
        return render(req, 'temple/interview_update.html', {
            'template_form': template_form,
            'formset': formset,
            'template': template
        })

    def post(self, req, pk):
        template = InterviewTemplate.objects.get(pk=pk)
        template_form = InterviewTemplateForm(req.POST, instance=template)
        QuestionFormSet = modelformset_factory(InterviewQuestion, form=InterviewQuestionForm, extra=0)
        formset = QuestionFormSet(req.POST, queryset=template.questions.all())

        if template_form.is_valid() and formset.is_valid():
            template = template_form.save(commit=False)
            template.created_by = req.user
            template.save()
            formset.instance = template
            formset.save()

            # 동적으로 추가된 질문들 처리
            self._save_dynamic_questions(req, template)

            return JsonResponse({'success': True, 'redirect': reverse('template:interview_detail', kwargs={'pk': template.pk})})
        else:
            return JsonResponse({'success': False, 'errors': {**template_form.errors, **formset.errors}}, status=400)

    def _save_dynamic_questions(self, req, template):
        questions = [v for k, v in req.POST.items() if k.startswith('questions[')]
        for question_text in questions:
            InterviewQuestion.objects.create(template=template, question_text=question_text)
    
class InterviewDeleteView(DeleteView):
    model = InterviewTemplate
    success_url = reverse_lazy('template:template_list')

    def delete(self, req, *args, **kwargs):
        response = super().delete(req, *args, **kwargs)
        if req.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'redirect': str(self.success_url)})
        return response
        

class EvaluationTemplateCreateView(View):
    def get(self, req):
        if req.user.is_authenticated:
            template_form = EvaluationTemplateForm()
            QuestionFormSet = modelformset_factory(EvaluationQuestion, form=EvaluationQuestionForm, extra=0)
            formset = QuestionFormSet(queryset=EvaluationQuestion.objects.none())
            return render(req, 'temple/evaluate_create.html', {
                'template_form': template_form,
                'formset': formset
            })
        else:
            return redirect("accounts:login")
            
    def post(self, req):
        if req.user.is_authenticated:
            template_form = EvaluationTemplateForm(req.POST)
            QuestionFormSet = modelformset_factory(EvaluationQuestion, form=EvaluationQuestionForm, extra=0)
            formset = QuestionFormSet(req.POST, queryset=EvaluationQuestion.objects.none())

            if template_form.is_valid() and formset.is_valid():
                template = template_form.save(commit=False)
                template.created_by = req.user
                template.save()
                
                questions_titles = [v for k, v in req.POST.items() if k.startswith('questions_titles[')]
                question_texts = [v for k, v in req.POST.items() if k.startswith('question_texts[')]
                
                if questions_titles and question_texts:
                    for title, text in zip(questions_titles, question_texts):
                        EvaluationQuestion.objects.create(template=template, question_title=title, question_text=text)
                
                formset_questions = formset.save(commit=False)
                for question in formset_questions:
                    question.template = template
                    question.save()
                
                return JsonResponse({'success': True, 'redirect': reverse('template:template_list')})
            else:
                errors = template_form.errors.as_json() if not template_form.is_valid() else formset.errors.as_json()
                return JsonResponse({'success': False, 'errors': errors}, status=400)
        else:
            return redirect("accounts:login")
    
class EvaluateDetailView(View):
    def get(self, req, pk):
        if req.user.is_authenticated:
            template = EvaluationTemplate.objects.get(pk=pk)
            questions = template.questions.all()
            return render(req, 'temple/evaluate_detail.html', {'template': template, 'questions':questions})
        else:
            return redirect("accounts:login")
        
class EvaluateUpdateView(View):
    def get(self, req, pk):
        template = EvaluationTemplate.objects.get(pk=pk)
        template_form = EvaluationTemplateForm(instance=template)
        QuestionFormSet = modelformset_factory(EvaluationQuestion, form=EvaluationQuestionForm, extra=0)
        formset = QuestionFormSet(queryset=template.questions.all())
        return render(req, 'temple/evaluate_update.html', {
            'template_form': template_form,
            'formset': formset,
            'template': template
        })

    def post(self, req, pk):
        template = EvaluationTemplate.objects.get(pk=pk)
        template_form = EvaluationTemplateForm(req.POST, instance=template)
        QuestionFormSet = modelformset_factory(EvaluationQuestion, form=EvaluationQuestionForm, extra=0)
        formset = QuestionFormSet(req.POST, queryset=template.questions.all())

        if template_form.is_valid() and formset.is_valid():
            template = template_form.save(commit=False)
            template.created_by = req.user
            template.save()
            formset.instance = template
            formset.save()

            # 동적으로 추가된 질문들 처리
            self._save_dynamic_questions(req, template)

            return JsonResponse({'success': True, 'redirect': reverse('template:evaluate_detail', kwargs={'pk': template.pk})})
        else:
            return JsonResponse({'success': False, 'errors': {**template_form.errors, **formset.errors}}, status=400)

    def _save_dynamic_questions(self, req, template):
        questions_titles = [v for k, v in req.POST.items() if k.startswith('questions_titles[')]
        question_texts = [v for k, v in req.POST.items() if k.startswith('question_texts[')]
        for title, text in zip(questions_titles, question_texts):
            EvaluationQuestion.objects.create(template=template, question_title=title, question_text=text)


class EvaluateDeleteView(DeleteView):
    model = EvaluationTemplate
    success_url = reverse_lazy('template:template_list')

    def delete(self, req, *args, **kwargs):
        response = super().delete(req, *args, **kwargs)
        if req.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'redirect': str(self.success_url)})
        return response