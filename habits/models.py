from django.conf import settings
from django.db import models


class Habit(models.Model):
    """Модель привычки"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Создатель',
        related_name='habits',
        blank=True,
        null=True
    )
    place = models.CharField(
        max_length=255,
        verbose_name='Место выполнения'
    )
    time = models.TimeField(
        verbose_name='Время выполнения'
    )
    action = models.CharField(
        max_length=255,
        verbose_name='Действие'
    )
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name='Признак приятной привычки'
    )
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Связанная привычка'
    )
    periodicity = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Периодичность (в днях)'
    )
    reward = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Вознаграждение'
    )
    time_to_complete = models.PositiveIntegerField(
        verbose_name='Время на выполнение (в секундах)'
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name='Признак публичности'
    )

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'

    def __str__(self):
        return f'Я буду {self.action} в {self.time} в {self.place}'
