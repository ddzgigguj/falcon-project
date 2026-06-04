from django.db import models
from django.conf import settings


class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='posts/')
    created_at = models.DateTimeField(auto_now_add=True)

    # Дополнительные поля для детального просмотра
    full_description = models.TextField(blank=True, help_text="Полное описание продукта")

    category = models.CharField(max_length=100, blank=True, help_text="Категория продукта")

    def __str__(self):
        return self.title

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # Один пользователь не может добавить один пост дважды

    def __str__(self):
        return f"{self.user.email} - {self.post.title}"