from django.contrib.auth.backends import BaseBackend
from _adminApp.models import Users


def userAuthenticate(request, username=None, password=None):
    try:
        
        if Users.objects.filter(username=username,password=password).exists():
            return Users.objects.get(username=username,password=password)
    except Users.DoesNotExist:
        return None

def get_user(user_id):
    try:
        return Users.objects.get(pk=user_id)
    except Users.DoesNotExist:
        return None
