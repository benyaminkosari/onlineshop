from django.db import models
from django.utils import timezone
from django.urls import reverse


class Post(models.Model):
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    text = models.TextField(max_length=5000)
    text_preview = models.TextField(max_length=400)
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to="blog/", blank=True)
    creating_date = models.DateTimeField(default=timezone.now)
    publishing_date = models.DateTimeField(null=True,blank=True)

    def publish(self):
        self.publishing_date = timezone.now()
        self.save()

    def approved_comments_set(self):
        return self.comments.filter(is_approved=True)

    def get_absolute_url(self):
        return reverse('blog:post_detail',kwargs={'pk':self.pk})

    def __str__(self):
        return self.title

class Comment(models.Model):
    class Meta:
        ordering = ('is_approved','-creating_date')

    author = models.CharField(max_length=30)
    text = models.TextField(max_length=200)
    email = models.EmailField()
    # Verify_exists???
    website = models.URLField(blank=True)
    post = models.ForeignKey('Post', related_name='comments' ,on_delete=models.CASCADE)
    creating_date = models.DateTimeField(default=timezone.now)
    is_approved = models.BooleanField(default=False)

    def approve(self):
        self.is_approved = True
        self.save()

    def get_absolute_url(self):
        return reverse('blog:post_list')

    def __str__(self):
        return self.text
