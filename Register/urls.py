from django.urls import path
from . import views


app_name = "Register"

urlpatterns = [
    path("Sigin/",views.SigninView.as_view(),name="register"),
    path("Login/", views.UserLoginView.as_view(), name="user_login"),
    path("Logout/", views.UserLogOutView.as_view(), name="user_logout"),
    path("profile/<int:user_id>",views.UserProfileView.as_view(),name="profile"),
    path("reset/", views.UserPassResetView.as_view(), name="reset_password"),
    path("reset/done/", views.UserPassRestDoneView.as_view(), name="password_reset_done"),
    path("confirm/<uidb64>/<token>", views.UserPassResetConfrim.as_view(), name="password_reset_confirm"),
    path("confirm/complete", views.UserPasswordRestCompleteView.as_view(), name="password_reset_complete"),
    path("follow/<int:user_id>", views.UserFollowView.as_view(), name="follow"),
    path("unfollow/<int:user_id>", views.UserUnFollowView.as_view(), name="unfollow"),

]