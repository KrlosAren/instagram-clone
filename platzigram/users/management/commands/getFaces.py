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

    def get_faces(self):

        api_key = 'V0Yk5h7hrpXBbKMn2QbmdeSSAx0LqdGC2P-TmTQznw8'
        url = f'https://api.unsplash.com/search/photos?page=1&query=faces&client_id={api_key}'
        img_urls = []
        response = requests.get(url)
        d = response.json()
        r = d['results']
        for i in r:
          img_urls.append(i['urls']['thumb'])
        print(img_urls)


        for url in img_urls:

            r = requests.get(url, stream=True)
            img_name = re.findall(
                'photo-[a-zAz0-9]{0,}-[a-zA-z0-9]{0,}', url)[0]
            file = os.path.join('media/faces', f'{img_name}.jpg')
            local_file = open(file, 'wb')
            local_file.write(r.content)
            local_file.close()

    def handle(self, *args,  **options):

        self.get_faces()

        # basepath = 'media/unplash'
