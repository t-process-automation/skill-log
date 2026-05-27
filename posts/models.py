from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Post(models.Model):
    CATEGORY_CHOICES = [
        ('english', 'English'),
        ('python', 'Python'),
        ('django', 'Django'),
        ('automation', 'Automation'),
        ('fx', 'FX'),
    ]

    title = models.CharField(max_length=200)
    body = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True
    )

    image = models.ImageField(
        upload_to='post_images/',
        blank=True,
        null=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:20]