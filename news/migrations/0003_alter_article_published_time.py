# Generated by Django 4.0.4 on 2022-06-02 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_alter_article_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='published_time',
            field=models.DateTimeField(),
        ),
    ]
