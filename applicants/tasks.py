from celery import shared_task
from .models import Application, Answer
from template.models import ApplicationQuestion

@shared_task
def process_application(application_id, answers):
    try:
        applyContent = Application.objects.get(id=application_id)

        for question_id, answer_text in answers.items():
            question = ApplicationQuestion.objects.get(id=question_id)
            Answer.objects.create(
                application = applyContent,
                question = question,
                answer_text = answer_text,
            )

        applyContent.status = 'submitted'
        applyContent.save()

        return f"Application {application_id} processed successfully"
    except Application.DoesNotExist:
        return f"Application {application_id} does not exist"
    except ApplicationQuestion.DoesNotExist:
        return f"Question {question_id} does not exist"