from django.contrib.auth.backends import ModelBackend
from .models import Applicant

class ApplicantBackend(ModelBackend):
      def authenticate(self, request, username=None, password=None, **kwargs):
         try:
            applicant = Applicant.objects.get(email=username)
            if applicant.check_password(password):
                  return applicant
         except Applicant.DoesNotExist:
            return None

      def get_user(self, user_id):
         try:
            return Applicant.objects.get(pk=user_id)
         except Applicant.DoesNotExist:
            return None