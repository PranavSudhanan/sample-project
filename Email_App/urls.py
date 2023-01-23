from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register),
    path('contact/', contact),
    path('registration/', reg),
    path('verify/<auth_token>', verify),
    path('login/', login)
]