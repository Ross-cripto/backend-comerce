from django.urls import path, include
from .views import *

urlpatterns = [
  path('register/', RegisterUserAPIView.as_view()), 
  path('login/', LoginView.as_view()), 
  path('change-password/', ChangePasswordView.as_view()),
  path('me/', ManageUserView.as_view()),
  path('activate/', VerifyCodeView.as_view()),
]
