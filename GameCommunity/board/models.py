from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name.username

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self) -> str:
        return self.name
    
    
class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    img = models.FileField(upload_to='images', null=True, blank=True, verbose_name='Изображение')
    
    def get_absolute_url(self): 
       return f'/adverts/{self.id}'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    commentText = models.TextField()
    commentCreated = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

 
    