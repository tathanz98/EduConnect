from django.db import models
from django.conf import settings

class Post(models.Model):
    CATEGORY_CHOICES = (
        ('investigación', 'Investigación'),
        ('eventos', 'Eventos'),
        ('dudas académicas', 'Dudas Académicas'),
        ('recursos', 'Recursos'),
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class StudyGroup(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_private = models.BooleanField(default=False)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_groups')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='study_groups', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class AcademicEvent(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_time = models.DateTimeField()
    link = models.URLField()
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organized_events')
    attendees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='attending_events', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)