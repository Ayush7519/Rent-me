from django.urls import path

from . import views

urlpatterns = [
    # USER ACCOUNT MANAGEMENT PATH.
    path(
        "register/",
        views.UserRegistrationView.as_view(),
        name="user registration path",
    ),
    path(
        "login/",
        views.UserLoginView.as_view(),
        name="user login path",
    ),
        path(
        "user-profile/",
        views.UserProfileView.as_view(),
        name="login user profile details view path",
    ),
        path(
        "password-change/",
        views.UserPasswordChangeView.as_view(),
        name="user password change path",
    ),
]