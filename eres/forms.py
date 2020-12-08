from django import forms
from .models import Post

class PostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ('title', 'file')

  def __init__(self, *args, **kwargs):
    super(PostForm, self).__init__(*args, **kwargs)
    self.fields['file'].required = True

  # def save(self, commit=True):
  #   self.instance = Post(**self.cleaned_data)
  #   if commit:
  #     self.instance.save()
  #   return self.instance