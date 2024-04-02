from django.db import models
from .model_user import User

class Releve(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField()
    temperature = models.IntegerField()