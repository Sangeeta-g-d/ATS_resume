from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import AgencyDetails


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

from django.contrib.auth.hashers import check_password

class AgencyAuthenticationBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            agency = AgencyDetails.objects.get(email=email)
            # Debugging: Print the retrieved agency's password
            print("Agency password:", agency.password)

            # Check if the provided password matches the stored password
            if check_password(password, agency.password):
                # Debugging: Print a message indicating successful authentication
                print("Authentication successful")
                return agency
            else:
                # Debugging: Print a message indicating password mismatch
                print("Password mismatch")
                return None
        except AgencyDetails.DoesNotExist:
            # Debugging: Print a message if the agency is not found
            print("Agency not found")
            return None
