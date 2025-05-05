from django.urls import path
from . import views


urlpatterns = [

    path("register/", views.RegisterAPIView.as_view()),
    path("code-verify/", views.CodeVerifyAPIView.as_view()),
    path("login/", views.LoginAPIView.as_view()),
    path("resend-code/", views.ResendCodeAPIView.as_view()),

    path("profile/", views.ProfileAPIView.as_view()),
    path("test/", views.APITEST.as_view())

]






