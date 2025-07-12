from django.contrib.auth.backends import ModelBackend
from travelapp.models import Client

class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = Client.objects.get(email=email)
            if user.check_password(password):
                return user
        except Client.DoesNotExist:
            return None