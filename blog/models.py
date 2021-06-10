from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.template.defaultfilters import slugify


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=250)
    category = models.CharField(max_length=50, default="")
    slug = models.SlugField(null=True, editable=False)
    content = RichTextUploadingField()
    author = models.CharField(max_length=25)
    post_date = models.DateTimeField(auto_now_add=True)
    draft_status = models.BooleanField(default=True)
    image = models.ImageField(upload_to="blog/images", default="")


    def __str__(self):
        if self.draft_status:
            return f'{self.title} - {self.category} - {self.author} - {self.post_date} ------- <  draft  >'
        else:
            return f'{self.title} - {self.category} - {self.author} - {self.post_date}'


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)
    

class BlogUser(User):

    class Meta:
        permissions = [
            ("blog_editor_status", "Can use the blog dashboard")
        ]