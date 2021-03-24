from django.urls.base import reverse_lazy
from posts.models import Post
from users.forms import SignupForm, profileForm
from users.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, resolve_url
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.db.utils import IntegrityError
from django.views.generic import DetailView, FormView, UpdateView


def login_view(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('posts:feed')
        else:
            return render(request, 'users/user_login.html', {'error': 'Invalid username and password'})

    return render(request, 'users/user_login.html')


@login_required
def logout_view(request):

    logout(request)
    return redirect('users:login')


# def register_view(request):

    # ?: USANDO FORMULARIOS MANUALES
    # VISTA DE UNA MANERA MAS MANUAL SIN FORMS ->
    # if request.method == 'POST':

    #     username = request.POST['username']
    #     password = request.POST['password']
    #     password2 = request.POST['password2']
    #     email = request.POST['email']
    #     first_name = request.POST['first_name']

    #     if password != password2:
    #         return render(request, 'users/register.html', {'error': 'Password confirmation does not match'})

    #     try:
    #         user = User.objects.create_user(
    #             username=username, password=password)
    #     except IntegrityError:
    #         return render(request, 'users/register_user.html', {'error': 'Username is already in use'})
    #     user.email = email
    #     user.first_name = first_name
    #     user.save()
    #     profile = Profile(user=user)
    #     profile.save()

    #     return redirect('user_login')

    # return render(request, 'users/register_user.html')

    # ? VISTA CON FORMS

    # if request.method == 'POST':
    #     form = SignupForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('users:login')
    # else:
    #     form = SignupForm()
    # return render(request, 'users/register_user.html', context={
    #     'form': form
    # })


# ?? class view form
class SignupView(FormView):
    template_name = 'users/register_user.html'
    form_class = SignupForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


# @login_required
# def update_profile(request):

#     form = profileForm()
#     profile = request.user.profile

#     if request.method == 'POST':
#         pass
#         form = profileForm(request.POST, request.FILES)
#         if form.is_valid():
#             print(form.cleaned_data)
#             data = form.cleaned_data

#             profile.website = data['website']
#             profile.phone_number = data['phone_number']
#             profile.biography = data['biography']
#             profile.picture = data['picture']

#             profile.save()
#             # messages.success(request, 'Your profile has been updated!')
#             url = reverse('users:detail', kwargs={
#                           'username': request.user.username})
#             return redirect(url)
#     else:
#         form = profileForm()

#     return render(request, 'users/update_profile.html', context={
#         'profile': profile,
#         'user': request.user,
#         'form': form
#     })


class UserDetailView(LoginRequiredMixin, DetailView):

    template_name = 'users/detail.html'
    queryset = User.objects.all()
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['posts'] = Post.objects.filter(
            user=user).order_by('-created_at')
        return context


class UpdateUserView(LoginRequiredMixin, UpdateView):

    template_name = 'users/update_profile.html'
    model = Profile
    fields = ['website', 'biography', 'phone_number', 'picture']

    def get_object(self):

        return self.request.user.profile

    def get_success_url(self):
        username = self.object.user.username
        return reverse('users:detail', kwargs={'username': username})


class LoginView(auth_views.LoginView):

    template_name = 'users/user_login.html'


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):

    template_name = 'users/logged_out.html'
