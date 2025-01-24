from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class SubFields(models.Model):
    is_published = models.BooleanField(
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.',
        default=True
    )
    created_at = models.DateTimeField(
        verbose_name='Добавлено',
        auto_now_add=True
    )

    class Meta:
        abstract = True


class Category(SubFields):
    title = models.CharField(
        verbose_name='Заголовок',
        max_length=256
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    slug = models.SlugField(
        'Идентификатор',
        help_text='Идентификатор страницы для URL; '
                  'разрешены символы латиницы, цифры, дефис и подчёркивание.',
        unique=True
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(SubFields):
    name = models.CharField(
        verbose_name='Название места',
        max_length=256
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Post(SubFields):
    title = models.CharField(
        verbose_name='Заголовок',
        max_length=256
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время '
                  'в будущем — можно делать отложенные публикации.'
    )
    author = models.ForeignKey(
        to=User,
        verbose_name='Автор публикации',
        on_delete=models.CASCADE
    )
    location = models.ForeignKey(
        to=Location,
        verbose_name='Местоположение',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    category = models.ForeignKey(
        to=Category,
        verbose_name='Категория',
        null=True,
        on_delete=models.SET_NULL
    )
    image = models.ImageField(
        verbose_name='Фото',
        upload_to='posts_images',
        blank=True
    )
    comment_count = models.IntegerField(
        verbose_name="Количество комментариев",
        default=0
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст комментария')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('created_at',)
