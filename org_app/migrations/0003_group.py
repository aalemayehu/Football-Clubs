# Generated by Django 2.2.5 on 2019-09-27 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('org_app', '0002_auto_20190927_0712'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='groups_created', to='org_app.User')),
                ('joiners', models.ManyToManyField(related_name='groups_joined', to='org_app.User')),
            ],
        ),
    ]
