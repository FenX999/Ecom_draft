from django.urls import path
from .views import crm_home

app_name='crm'

urlpatterns = [
    path('home/', crm_home, name='crm-home' ),
    # path('login', crm_login, name='crm-login')
]
