from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post,Comment
from shop import models
from blog.forms import PostForm, CommentForm
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView,DeleteView)


# class HomeView(TemplateView):
#     template_name = 'home.html'

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(publishing_date__lte=timezone.now()).order_by('-publishing_date')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['main_categories'] = models.Category.objects.filter(is_main=True)
        return context

class PostDetailView(DetailView):
    model = Post

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['main_categories'] = models.Category.objects.filter(is_main=True)
        context['comment_form'] = CommentForm()
        return context

    def post(self, *args, **kwargs):
        form = CommentForm(self.request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            post = get_object_or_404(Post,id=self.kwargs['pk'])
            comment.post = post
            form.save(commit=True)
        else:
            print("*** INVALID FORM ***")
        return redirect('blog:post-detail', pk=self.kwargs['pk'])

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    form_class = PostForm

class PostUpdateView(LoginRequiredMixin,UpdateView):
    model = Post
    form_class = PostForm

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('blog:post_list')

class DraftListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'blog/post_draft_list.html'

    def get_queryset(self):
        return Post.objects.filter(publishing_date__isnull=True,creating_date__lte=timezone.now()).order_by('-creating_date')

class CommentCreateView(CreateView):
    model = Comment
    template_name = 'blog/post_detail.html'
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        post = get_object_or_404(Post,id=self.kwargs['pk'])
        comment.post = post
        return super(CommentCreateView, self).form_valid(form)

class CommentDeleteView(LoginRequiredMixin,DeleteView):
    model = Comment
    template_name = 'blog/comment_delete.html'

    def get_success_url(self):
        comment = get_object_or_404(Comment,pk=self.kwargs['pk'])
        print(comment.post.id)
        return reverse_lazy('blog:post_detail',kwargs={'pk':comment.post.id})

@login_required
def post_publishing(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('blog:post_detail',pk=pk)

@login_required
def approve_comment_view(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('blog:post_detail',pk=comment.post.pk)
