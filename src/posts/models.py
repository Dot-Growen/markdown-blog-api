from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.db import models
from django.utils.text import slugify

User = get_user_model()

def upload_post_image(instance, filename):
    return f"{instance.user}/{filename}"

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=300)
    content = models.TextField() # markdown
    thumbnail = models.ImageField(upload_to=upload_post_image)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

def pre_save_receiver(sender, instance, **kwargs):
        if not instance.slug:
            instance.slug = slugify(instance.title)
            
pre_save.connect(pre_save_receiver, sender=Post)
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
    
class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
