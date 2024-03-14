
from django.urls import path 
from .views import *


urlpatterns = [
    path('', Home4, name='home'),
]
