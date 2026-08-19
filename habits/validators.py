from rest_framework.serializers import ValidationError


class RewardOrRelatedHabitValidator:
    """Исключает одновременный выбор связанной привычки и указания вознаграждения."""

    def __call__(self, value):
        related_habit = value.get('related_habit')
        reward = value.get('reward')

        if related_habit and reward:
            raise ValidationError(
                'Нельзя одновременно указывать связанную привычку и вознаграждение.'
            )


class ExecutionTimeValidator:
    """Время выполнения должно быть не больше 120 секунд."""

    def __init__(self, max_time=120):
        self.max_time = max_time

    def __call__(self, value):
        time_to_complete = value.get('time_to_complete')
        if time_to_complete and time_to_complete > self.max_time:
            raise ValidationError(
                f'Время выполнения не должно превышать {self.max_time} секунд.'
            )


class RelatedHabitIsPleasurableValidator:
    """В связанные привычки могут попадать только привычки с признаком приятной привычки."""

    def __call__(self, value):
        related_habit = value.get('related_habit')
        if related_habit and not related_habit.is_pleasant:
            raise ValidationError(
                'В качестве связанной привычки может быть выбрана только приятная привычка.'
            )


class PleasantHabitValidator:
    """У приятной привычки не может быть вознаграждения или связанной привычки."""

    def __call__(self, value):
        is_pleasant = value.get('is_pleasant')
        reward = value.get('reward')
        related_habit = value.get('related_habit')

        if is_pleasant:
            if reward or related_habit:
                raise ValidationError(
                    'У приятной привычки не может быть вознаграждения или связанной привычки.'
                )


class PeriodicityValidator:
    """Нельзя выполнять привычку реже, чем 1 раз в 7 дней (периодичность не более 7 дней)."""

    def __init__(self, max_period=7):
        self.max_period = max_period

    def __call__(self, value):
        periodicity = value.get('periodicity')
        if periodicity and periodicity > self.max_period:
            raise ValidationError(
                f'Нельзя выполнять привычку реже, чем 1 раз в {self.max_period} дней.'
            )