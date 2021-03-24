import os
from posts.models import Post
from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth.models import User
import random
import requests
from PIL import Image
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import re
from django.core.files import File
from django.core.files.images import ImageFile


class Command(BaseCommand):

    help = "Create post to database"

    def get_data(self):

        api_key = 'V0Yk5h7hrpXBbKMn2QbmdeSSAx0LqdGC2P-TmTQznw8'
        url = f'https://api.unsplash.com/photos/?client_id={api_key}'

        img_urls = []
        response = requests.get(url)
        data = response.json()
        for img in data:
            img_urls.append(img['urls']['small'])

        for url in img_urls:

            r = requests.get(url, stream=True)
            img_name = re.findall(
                'photo-[a-zAz0-9]{0,}-[a-zA-z0-9]{0,}', url)[0]
            file = os.path.join('media/unplash', f'{img_name}.jpg')
            local_file = open(file, 'wb')
            local_file.write(r.content)
            local_file.close()

    def handle(self, *args,  **options):

        # self.get_data()

        basepath = 'media/unplash'
        imgs = []
        for entry in os.listdir(basepath):
            if os.path.isfile(os.path.join(basepath, entry)):
                imgs.append(entry)
                print(entry)

        fake = Faker(['es_ES'])
        users = User.objects.all()

        for _ in range(50):
            user = random.choice(users)
            post = {
                'title': fake.text(max_nb_chars=20),
                'user': user,
                'profile': user.profile,
            }
            img = random.choice(imgs)
            new_post = Post.objects.create(**post)
            f = File(open(os.path.join('media/unplash', img), 'rb'))
            new_post.photo.save(f'{img}', f)
            new_post.slug = new_post.get_slug()
            new_post.save()
            print(new_post)
