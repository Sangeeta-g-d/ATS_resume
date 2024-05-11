# backends.py

from django.contrib.auth.backends import ModelBackend
from .models import NewUser
from django.contrib.auth import get_user_model


class CustomAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class CustomBackend(ModelBackend):
    def authenticate(self, request, email=None):
        try:
            user = NewUser.objects.get(email=email)
        except NewUser.DoesNotExist:
            return None
        return user

