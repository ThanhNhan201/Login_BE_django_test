# Generated by Django 4.1.7 on 2023-03-23 06:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comic', '0008_alter_comic_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chap',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('removed', models.BooleanField(default=False)),
                ('edited', models.BooleanField(default=False)),
                ('chap', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comic.chap', to_field='name')),
                ('comic', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comic', to='comic.comic')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
