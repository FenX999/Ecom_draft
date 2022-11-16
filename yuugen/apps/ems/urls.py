from django.urls import path
from . import views

app_name='ems'


urlpatterns=[
    path('', views.ems_index, name='ems-home'),
    path('create-profile/', views.create_staff_views, name="profile-creator")
]