# Generated by Django 5.0 on 2024-01-27 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='blog_pdf',
            field=models.FileField(blank=True, upload_to='blog_pdfs'),
        ),
    ]
