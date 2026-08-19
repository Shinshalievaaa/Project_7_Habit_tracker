from rest_framework import serializers
from habits.models import Habit
from habits.validators import (
    ExecutionTimeValidator,
    PeriodicityValidator,
    PleasantHabitValidator,
    RelatedHabitIsPleasurableValidator,
    RewardOrRelatedHabitValidator,
)


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Habit с валидаторами."""

    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('user',)
        validators = [
            RewardOrRelatedHabitValidator(),
            ExecutionTimeValidator(),
            RelatedHabitIsPleasurableValidator(),
            PleasantHabitValidator(),
            PeriodicityValidator(),
        ]
