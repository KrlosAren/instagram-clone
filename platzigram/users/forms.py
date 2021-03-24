from users.models import Profile
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.query import ValuesIterable


class profileForm(forms.Form):

    website = forms.URLField(max_length=200, required=True)
    biography = forms.CharField(max_length=500, required=False)
    phone_number = forms.CharField(max_length=20, required=False)
    picture = forms.ImageField()


class SignupForm(forms.Form):

    username = forms.CharField(label=False, min_length=4, max_length=50, widget=forms.TextInput(
        attrs={'placeholder': 'Username', 'class': 'form-control mt-4', 'required': True, 'autofocus': True}))

    email = forms.CharField(label=False, min_length=4, max_length=50, widget=forms.EmailInput(
        attrs={'placeholder': 'Email', 'class': 'form-control mt-4', 'required': True}))

    first_name = forms.CharField(label=False, min_length=4, max_length=50, widget=forms.TextInput(
        attrs={'placeholder': 'Firstname', 'class': 'form-control mt-4', 'required': True}))

    password = forms.CharField(label=False, min_length=4, max_length=50, widget=forms.PasswordInput(
        attrs={'placeholder': 'Password', 'class': 'form-control mt-4', 'required': True}))
    password2 = forms.CharField(label=False, min_length=4, max_length=50, widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm Password', 'class': 'form-control mt-4', 'required': True}))

    def clean_username(self):

        username = self.cleaned_data['username']
        q = User.objects.filter(username=username).exists()

        if q:
            raise forms.ValidationError('Username is already in use.')
        return username

    def clean(self):
        data = super().clean()

        password = data['password']
        password2 = data['password2']

        if password != password2:
            raise forms.ValidationError('Passwords do not match')
        return data

    def save(self):

        data = self.cleaned_data
        data.pop('password2')

        user = User.objects.create_user(**data)
        profile = Profile(user=user)
        profile.save()
