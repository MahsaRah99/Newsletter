# Generated by Django 4.2.7 on 2023-11-26 13:38

import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='subcategories', to='contents.category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('body', models.TextField(help_text='Post content', verbose_name='Body')),
                ('image', models.FileField(upload_to='uploads/posts/')),
                ('status', models.CharField(choices=[('D', 'Draft'), ('P', 'Published'), ('UP', 'Unpublished')], default='D', max_length=2)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cat_posts', to='contents.category')),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pub_posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
            },
            bases=(models.Model, core.models.TimeStampMixin),
        ),
        migrations.CreateModel(
            name='ArchievedPost',
            fields=[
            ],
            options={
                'proxy': (True,),
                'indexes': [],
                'constraints': [],
            },
            bases=('contents.post',),
        ),
    ]
