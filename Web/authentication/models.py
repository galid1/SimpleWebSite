from django.db import models

# Create your models here.
class WebUser(models.Model):
    user_id = models.CharField(max_length=10)
    user_pw = models.CharField(max_length=10)

class Board(models.Model):
    board_title = models.CharField(max_length=30)
    board_contents = models.CharField(max_length=200)
    board_date = models.DateField(auto_now=True)
    board_writer = models.ForeignKey(WebUser, models.CASCADE)