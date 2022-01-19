from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post

class PostListView(ListView):
    template_name = "blog/list.html"
    model = Post


class PostDetailView(DetailView):
    template_name = "blog/detail.html"
    model = Post 

class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = "blog/new.html"
    model = Post
    fields = ['title', 'author', 'body']