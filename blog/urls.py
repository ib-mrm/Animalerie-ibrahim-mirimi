from django.urls import path
from . import views

urlpatterns = [
    path('', views.animal_list, name='animal_list'),
]
