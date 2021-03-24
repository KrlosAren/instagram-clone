from posts.apps import PostsConfig
from django.contrib import admin

# Register your models here.


from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ('user', 'title', 'photo', 'created_at', 'updated_at')

    list_display_links = ('user', 'title', 'photo')

    search_fields = ('created_at', 'updated_at', 'user')

    list_filter = ('created_at', 'updated_at', 'user')

    readonly_fields = ('user', 'created_at', 'updated_at')
