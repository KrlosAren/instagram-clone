
from django.contrib.auth.mixins import LoginRequiredMixin
from posts.forms import PostForm
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
# Create your views here.
from django.views.generic import ListView,  CreateView, DetailView

from .models import Post

# ? forma de renderizar una lista de data con vistas en funciones
# @login_required
# def list_post(request):

#     posts = Post.objects.all().order_by('-created_at')

#     context = {
#         'posts': posts,
#         'title': 'Platzigram | Feed'
#     }
#     return render(request, 'posts/posts_list.html', context=context)

# ? clss view


class PostsFeedView(LoginRequiredMixin, ListView):

    template_name = 'posts/posts_list.html'
    model = Post
    ordering = ('-created_at')
    paginate_by = 10
    context_object_name = 'posts'


class CreatePostView(LoginRequiredMixin, CreateView):

    template_name = 'posts/new_post.html'
    form_class = PostForm
    success_url = reverse_lazy('posts:feed')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['profile'] = self.request.user.profile

        return context

        # @login_required
        # def new_post(request):

        #     if request.method == 'POST':

        #         form = PostForm(request.POST, request.FILES)
        #         if form.is_valid():
        #             import pdb; pdb.set_trace()
        #             data = form.cleaned_data
        #             post = Post.objects.create(**data)
        #             post.slug = post.get_slug()
        #             post.save()

        #         return redirect('posts:feed')
        #     else:

        #         form = PostForm()

        #     return render(
        #         request=request,
        #         template_name='posts/new_post.html',
        #         context={
        #             'form': form,
        #             'user': request.user,
        #             'profile': request.user.profile,
        #             'title': 'Create a Post'
        #         }
        #     )


class DetailPost(LoginRequiredMixin, DetailView):

    template_name = 'posts/detail.html'
    model = Post
    queryset = Post.objects.all()
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['post'] = Post.objects.filter(pk=post.pk, user=post.user_id)[0]
        # import pdb; pdb.set_trace()
        return context
