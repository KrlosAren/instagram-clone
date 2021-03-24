from django.urls import path
from users import views
from django.views.generic import TemplateView

urlpatterns = [
    path(
        route='login/',
        view=views.LoginView.as_view(),
        name='login'),

    path(
        route='logout/',
        view=views.LogoutView.as_view(),
        name='logout'),


    path(
        route='register/',
        view=views.SignupView.as_view(),
        name='register'),


    path(
        route='me/profile',
        view=views.UpdateUserView.as_view(),
        name='profile'),

    path(
        route='<str:username>',
        view=views.UserDetailView.as_view(),
        name='detail'),

]
