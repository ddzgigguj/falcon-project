# Generated migration file
# Run: python manage.py makemigrations posts
# Then: python manage.py migrate

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.CharField(blank=True, help_text='Категория продукта', max_length=100),
        ),
        migrations.AddField(
            model_name='post',
            name='full_description',
            field=models.TextField(blank=True, help_text='Полное описание продукта'),
        ),
        migrations.AddField(
            model_name='post',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Цена продукта', max_digits=10, null=True),
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'post')},
            },
        ),
    ]