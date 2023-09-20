from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.views.generic.edit import FormMixin
from .filters import PostFilter
from .utils import send_notification_email
from .forms import PostForm, MessageForm, MessageAccept
from .models import Post, Comment, Author
from django.urls import resolve


class AdvertView(ListView):
    model = Post
    ordering = ['-created_at']
    template_name = 'adverts/posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context    


class AdvertDetail(FormMixin, DetailView):
    model = Post
    template_name = 'adverts/post.html'
    context_object_name = 'post'
    form_class = MessageForm
    success_url = reverse_lazy('board:allAdverts')

    def get_context_data(self, **kwargs):
        context = super(AdvertDetail, self).get_context_data(**kwargs)
        author_post = Post.objects.get(id=self.kwargs['pk'])
        context['is_author'] = author_post
        context['form'] = MessageForm(initial={'commentPost': self.object, 'commentUser':self.request.user})
        context['responses'] = Comment.objects.filter(commentPost = self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comm = form.save(commit=False)
        comm.commentUser = self.request.user
        comm.commentPost = Post.objects.get(id=self.kwargs['pk'])
        comm.save()
        return super().form_valid(form)
    
    
class CommentAccept(UpdateView):
    model = Comment
    form_class = MessageAccept
    template_name = 'inc/post_comment.html'
    success_url= '/profile/responses'

    def form_valid(self, form):
        message = form.save(commit=False)
        message.is_accepted=True
        message.save()
        subject = 'Ваш комментарий был принят'
        message_text = f'Ваш комментарий к посту "{ message.commentPost.title }" был принят.'
        send_notification_email(message.commentUser.email, subject, message_text)
        return super().form_valid(form)

class CommentDelete(DeleteView):
    model = Comment
    success_url = reverse_lazy('board:responses')
    

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context
    

class ProfileList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'profile/profile_responses.html'
    context_object_name = 'post_search'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        author = Author.objects.get(name=self.request.user).id 
        posts = Post.objects.all().filter(author=author).order_by('-created_at')
        context['posts'] = posts
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        context['filter'] = PostFilter(self.request.GET, queryset = posts)
        context['form'] = PostForm()
        return context


class ProfileMessageView(ListView):
    model = Post
    template_name = 'profile/profile_messages.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        comments = Comment.objects.all().filter(commentUser=user).order_by('-commentCreated')
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        context["messages"] = comments
        return context


class AdvertCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'adverts/post_create.html'
    permission_required = ('board.add_post',
                            'board.change_post')
    permission_denied_message = 'Чтобы создавать новости, необходимо стать автором'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = Author.objects.get(name = self.request.user)
        context['form'] = PostForm(initial={'author': author.name})
        return context


class AdvertUpdateView(LoginRequiredMixin,  UpdateView):
    template_name = 'adverts/post_create.html'
    form_class = PostForm
    permission_required = ('board.add_post',
                            'board.change_post')

    def get_object(self, **kwargs):
       id = self.kwargs.get('pk')
       return Post.objects.get(pk=id)


class AdvertDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'adverts/post_delete.html'
    permission_required = ('board.delete_post')
    queryset = Post.objects.all()
    success_url = reverse_lazy('board:allAdverts')


@login_required
def upgrade_me(request):
    user = request.user
    Author.objects.create(name=user)
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/')