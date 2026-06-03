from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image

class News(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    content = models.TextField('Содержание')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='news')
    created_date = models.DateTimeField('Дата публикации', default=timezone.now)
    image = models.ImageField('Изображение', upload_to='news_images/', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_date']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 400 or img.width > 600:
                output_size = (600, 400)
                img.thumbnail(output_size)
                img.save(self.image.path)

class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, verbose_name='Новость', related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='comments')
    text = models.TextField('Текст комментария')
    created_date = models.DateTimeField('Дата создания', default=timezone.now)
    is_active = models.BooleanField('Активен', default=True)
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_date']
    
    def __str__(self):
        return f'Комментарий от {self.author.username} к {self.news.title}'