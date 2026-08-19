from django.urls import path
from habits.apps import HabitsConfig
from habits.views import (
    HabitCreateAPIView,
    HabitDestroyAPIView,
    HabitListAPIView,
    HabitRetrieveAPIView,
    HabitUpdateAPIView,
    PublicHabitListAPIView,
)

app_name = HabitsConfig.name

urlpatterns = [
    path('', HabitListAPIView.as_view(), name='habit-list'),
    path('public/', PublicHabitListAPIView.as_view(), name='public-habit-list'),
    path('create/', HabitCreateAPIView.as_view(), name='habit-create'),
    path('<int:pk>/', HabitRetrieveAPIView.as_view(), name='habit-detail'),
    path('<int:pk>/update/', HabitUpdateAPIView.as_view(), name='habit-update'),
    path('<int:pk>/delete/', HabitDestroyAPIView.as_view(), name='habit-delete'),
]
