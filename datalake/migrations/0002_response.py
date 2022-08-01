# Generated by Django 4.0.3 on 2022-07-25 14:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('datalake', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phrase', models.CharField(max_length=1000)),
                ('create_date', models.DateTimeField()),
                ('CategoryDepth', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datalake.categorydepth')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('intent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datalake.intent')),
            ],
        ),
    ]