from django.db import models

# Create your models here.

class Post(models.Model):
  title = models.CharField(max_length=200, null=False)
  contents = models.TextField()
  category = models.CharField(max_length=100, null=False)
  create_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'{self.title}-{self.create_at}'