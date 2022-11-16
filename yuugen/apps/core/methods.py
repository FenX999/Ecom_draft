from django.http import request


def get_current_user(self, request):
    return  self.request.user.id

def get_current_user_email(self, request):
    return str(self.request.user)