from posts.models import Post
from users.models import Profile
from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth.models import User
from random import random, randint


class Command(BaseCommand):

    help = "Create user to database"

    def handle(self, *args,  **options):

        fake = Faker(['es_ES'])


        for _ in range(20):
            n = randint(102, 141)
            user = User.objects.get(id=n)

            profile = {
                'user': user,
                'website': fake.url(),
                'biography': fake.paragraph(nb_sentences=5, variable_nb_sentences=False),
                'phone_number': fake.phone_number(),
                'picture': 'https://dummyimage.com/200x200.jpg?text=user-profile',
            }

            userProfile = Profile.objects.create(**profile)
            userProfile.save()
            print(userProfile)
