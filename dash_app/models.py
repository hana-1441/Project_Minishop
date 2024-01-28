from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

class Blog(models.Model):
    title=models.CharField(max_length=100)
    desc=RichTextField()
    image=models.ImageField(upload_to='blog_images',blank=True)
    blog_pdf=models.FileField(upload_to='blog_pdfs',blank=True)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)
    
    def __str__(self):
        return self.title