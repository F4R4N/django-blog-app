# Generated by Django 3.0.7 on 2020-07-08 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20200708_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='comment',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='comment',
            name='name',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='newslettersubscriber',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='newslettersubscriber',
            name='last_name',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='newslettersubscriber',
            name='name',
            field=models.CharField(max_length=60),
        ),
        migrations.CreateModel(
            name='NewsPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('users', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.NewsLetterSubscriber')),
            ],
        ),
    ]