from django.db import models
from django.db.models.deletion import CASCADE
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.

class Fact(models.Model):
  title = models.CharField(max_length=50)
  description = models.TextField(max_length=500)
  likes = models.IntegerField(default = 0,)
  author = models.ForeignKey(User, on_delete=CASCADE)

  class Meta:
    ordering = ['-likes']

  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse("fact_detail", kwargs={"pk": self.pk})

class Photo(models.Model):
  url = models.CharField(max_length=100)
  fact = models.OneToOneField(Fact, on_delete=CASCADE)