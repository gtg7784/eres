import string
from random import choice
from django.db import models

def user_path(instance, filename):
  pid = ''.join([choice(string.ascii_letters) for _ in range(8)])
  extension = filename.split('.')[-1]
  return f'{instance.author}/{pid}.{extension}'

class Post(models.Model):
  title = models.CharField(max_length=200, help_text="포스팅의 제목")
  contents = models.TextField(help_text="포스팅의 내용")
  category = models.CharField(max_length=100, help_text="포스팅의 카테고리")
  author = models.CharField(max_length=200, help_text="포스팅을 올린 사람 (user.username)")
  file = models.ImageField(upload_to=user_path)
  create_at = models.DateTimeField(auto_now_add=True, help_text="생성된 시간 (title)")

  def __str__(self):
    return f'{self.title}-{self.create_at}'