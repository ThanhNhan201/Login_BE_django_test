# Generated by Django 4.1.7 on 2023-03-23 06:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comic', '0012_comment_alter_chap_name_delete_usercomment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='chap',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comic.chap'),
        ),
    ]
