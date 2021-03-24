import os

from django.core.files.base import File
from posts.models import Post
from users.models import Profile
from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth.models import User
import random


class Command(BaseCommand):

    help = "Create user to database"

    def handle(self, *args,  **options):
        basepath = 'media/faces'
        faces = []
        for entry in os.listdir(basepath):
            if os.path.isfile(os.path.join(basepath, entry)):
                faces.append(entry)

        fake = Faker(['es_ES'])
        for _ in range(10):
            user = {
                'username': fake.user_name(),
                'first_name': fake.first_name(),
                'email': fake.email(),
                'password': fake.paragraph(nb_sentences=2)
            }
            new_user = User.objects.create_user(**user)
            new_user.save()
            p = {
                'user': new_user,
                'website': fake.url(),
                'biography': fake.paragraph(nb_sentences=5, variable_nb_sentences=False),
                'phone_number': fake.phone_number(),
            }
            profile = Profile(**p)
            face = random.choice(faces)
            f = File(open(os.path.join('media/faces', face), 'rb'))
            profile.picture.save(f'{face}', f)
            profile.save()
            print(f'{new_user} :  {profile}')

