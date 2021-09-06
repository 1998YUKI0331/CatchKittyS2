from django.db import models

# Create your models here.

class InputTemp(models.Model):
    keyword = models.CharField(max_length=2000)
    max_price = models.BigIntegerField()

class Input(models.Model): #예약한 사람들 정보
    nickname = models.CharField(max_length=2000)
    callnumber = models.CharField(max_length=2000)
    keyword = models.CharField(max_length=2000)
    max_price = models.BigIntegerField()