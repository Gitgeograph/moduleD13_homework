from django.forms import ModelForm
from allauth.account.forms import SignupForm, LoginForm
from django.contrib.auth.models import Group
from django import forms
from .models import Post, Comment


class PostForm(ModelForm):
    
    class Meta:
        model = Post
        fields = ("author","img", "title", "category", 'text')
        widgets = {
            'author': forms.Select(attrs={
            'class': 'border border-gray-200 rounded text-base font-medium leading-none py-3 w-full pl-3 mb-3',           
            }),
            'title': forms.TextInput(attrs={
            'class': 'mt-1 w-full rounded-md border-gray-200 shadow-sm sm:text-sm',
            'placeholder': 'Enter title'
            }),
            "category": forms.CheckboxSelectMultiple(attrs={
            "class": 'flex-check',
            }),
            'text': forms.Textarea(attrs={
            'class': 'mt-1 w-full rounded-md border-gray-200 shadow-sm sm:text-sm',
            }),
        }


class MessageForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('commentText', 'commentPost', 'commentUser')

        widgets = {
            'commentText':  forms.Textarea(attrs={
                'class':'w-4/5  bg-gray-300 rounded-lg border-gray-200 shadow-sm sm:text-sm',
                'placeholder': 'Написать комментарий...',
                }),
            'commentPost': forms.HiddenInput(),
            'commentUser': forms.HiddenInput(),
            'is_accepted': forms.HiddenInput(),
        }

class MessageAccept(ModelForm):
    class Meta:
        model = Comment
        fields = ['is_accepted']


class BasicSignupForm(SignupForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email', 'class':'border rounded border-gray-200 text-base font-medium leading-none py-3 w-full pl-3 mb-3',}))
  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({"class": "border border-gray-200 rounded text-base font-medium leading-none py-3 w-full pl-3 mb-3"})
        self.fields["password2"].widget.attrs.update({"class": "border border-gray-200 rounded text-base font-medium leading-none py-3 w-full pl-3 mb-3"})
    
  
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get_or_create(name='common')[0]
        basic_group.user_set.add(user)
        return user
    

class BasicLoginForm(LoginForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'border border-gray-200 rounded text-base font-medium leading-none py-3 w-full pl-3'}))
            
    def __init__(self, *args, **kwargs):
        super(BasicLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget = forms.TextInput(attrs={'class':'border border-gray-200 rounded text-base font-medium leading-none py-3 w-full pl-3'})

    def save(self, request):
        user = super(BasicLoginForm, self).save(request)
        basic_group = Group.objects.get_or_create(name='common')[0]
        basic_group.user_set.add(user)
        return user