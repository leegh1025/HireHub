import openai
from dotenv import load_dotenv
import os
from django.shortcuts import render,redirect
from applicants.models import Application, Answer

# .env 파일 로드
load_dotenv()

# OpenAI API 키 설정
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_questions(request, application_id):
    if request.user.is_authenticated:
        application = Application.objects.get(pk=application_id)
        answers = application.answers.all()

        content = ""
        for answer in answers:
            content += f"Q: {answer.question.question_text}\n"
            content += f"A: {answer.answer_text}\n\n"

        completion = openai.chat.completions.create(
            model='gpt-4o',  
            messages=[
                {"role": "system", "content": "You are an interview assistant. Based on the content of the candidate's application, generate relevant and insightful interview questions that could help assess their fit for the role."},
                {"role": "user", "content": content}
            ],
            max_tokens=700,
            temperature=0.5
        )

        questions = completion.choices[0].message.content
        questions = questions.replace("\n\n", "</p><p>").replace("\n", "<br>")
        questions = f"<p>{questions}</p>"

        return render(request, 'applicant/openai.html', {'questions': questions})
    else:
        return redirect("accounts:login")
    