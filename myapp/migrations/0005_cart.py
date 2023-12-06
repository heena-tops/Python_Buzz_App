# Generated by Django 4.2.6 on 2023-11-24 06:32

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_blog_comment_comment_count_blog_comment_like_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(default=datetime.datetime(2023, 11, 24, 6, 32, 9, 340281, tzinfo=datetime.timezone.utc), null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.user')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.package')),
            ],
        ),
    ]
