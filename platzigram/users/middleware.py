

from django.shortcuts import redirect

# con reverse puedo usar las urls con sus nombres puestos en urls.py
from django.urls import reverse


class ProfileCompletionMiddleware:
    """
    Ensure every user that i interacting with the plaform
    have their profile picture and biography
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if not request.user.is_anonymous and request.user.is_staff != True:
            profile = request.user.profile
            # profile.user
            # user.profile

            if not profile.picture or not profile.biography:

                # if request.path != reverse('update_profile'):
                if request.path not in [reverse('users:profile'), reverse('users:logout')]:

                    return redirect('users:profile')

        response = self.get_response(request)
        return response
