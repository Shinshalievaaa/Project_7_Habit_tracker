from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer


class HabitListAPIView(ListAPIView):
    """Список привычек текущего пользователя с пагинацией."""
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user).order_by('id')


class PublicHabitListAPIView(ListAPIView):
    """Список публичных привычек."""
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Habit.objects.filter(is_public=True).order_by('id')


class HabitCreateAPIView(CreateAPIView):
    """Создание привычки (автоматически привязывает текущего пользователя)."""
    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitRetrieveAPIView(RetrieveAPIView):
    """Детальный просмотр привычки владельцем."""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)


class HabitUpdateAPIView(UpdateAPIView):
    """Редактирование привычки владельцем."""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)


class HabitDestroyAPIView(DestroyAPIView):
    """Удаление привычки владельцем."""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)
    