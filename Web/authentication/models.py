from django.db import models

# Create your models here.
class WebUser(models.Model):
    user_id = models.CharField(max_length=10)
    user_pw = models.CharField(max_length=10)

class Board(models.Model):
    title = models.CharField(max_length=30)
    contents = models.CharField(max_length=200)
    date = models.DateField(auto_now=True)
    writer = models.ForeignKey(WebUser, models.CASCADE)