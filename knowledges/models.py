from django.db import models
from django.conf import settings

# Create your models here.


class Article(models.Model):
    url = models.URLField()
    tags = models.ManyToManyField('Tag', related_name='tagged_articles')
    comment = models.TextField()
    creator = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Tag(models.Model):
    label = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"({self.id}) {self.label}"
