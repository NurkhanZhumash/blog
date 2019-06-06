from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (ListView, DetailView, View)

from django.views.generic.edit import UpdateView, DeleteView,CreateView

from blog.forms import CommentForm
from blog.models import Post

from django.urls import reverse_lazy


class ListPostView(ListView):
    model = Post
    template_name = 'list_post.html'
    paginate_by = 1
    dataset = Post.objects.all()

class DetailPostView(DetailView):
    model = Post
    template_name = 'detail_post.html'

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ('title','short_notation','content')
    template_name = 'update_post.html'
    login_url = 'login'

    def get_user(self):
        return self.request.user

    def test_func(self):
        p = self.get_object()
        return p.author == self.request.user

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('list_post')
    login_url = 'login'

    def test_func(self):
        p = self.get_object()
        return p.author == self.request.user

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ('title','short_notation','content')
    login_url = 'login'
    template_name = 'create_post.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

def comment_create_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form})


