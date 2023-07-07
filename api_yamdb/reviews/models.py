from django.db import models


class Category(models.Model):
    """Модель для категорий."""
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(unique=True,
                            verbose_name='Адрес типа slug')

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель для жанров."""
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(unique=True,
                            verbose_name='Адрес типа slug')

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель для произведений."""
    name = models.CharField(max_length=200, verbose_name='Название')
    year = models.IntegerField(verbose_name='Год выпуска')
    rating = models.IntegerField(null=True, default=None)
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='titles',
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
    )


class GenreTitle(models.Model):
    """
    Вспомогательная модель.
    Для реализаци связи М2М между моделями Title и Genre.
    """
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'
