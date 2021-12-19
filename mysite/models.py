from django.db import models

class MyUser(models.Model):
  email = models.EmailField(max_length=100)
  name = models.CharField(max_length=100, unique=True)
  password = models.CharField(max_length=100)

class Gift(models.Model):
  name = models.CharField(max_length=100)
  owner = models.ForeignKey(MyUser, on_delete=models.CASCADE)
