from django.db import models
class Users(models.Model):
	email = models.EmailField(max_length=255)
	password = models.CharField(max_length=50)

class Post(models.Model):
    title = models.CharField(max_length=50, default="")
    description = models.TextField(default="")

    def __str__(self):
        return self.title
