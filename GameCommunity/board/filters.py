import django_filters as filters
from django_filters import FilterSet
from django import forms
from .models import Post

class PostFilter(FilterSet):

    title = filters.CharFilter(
        label='', 
        lookup_expr='icontains',
        widget = forms.TextInput(attrs={
            'placeholder': 'Title', 
            'class':'border w-5/6 mb-3 border-gray-200 rounded-md text-base font-medium leading-none py-3 pl-3 mb-3',        
        }))    

    class Meta:
        model = Post
        fields = ('title',)