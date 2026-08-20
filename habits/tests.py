from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit

User = get_user_model()


class HabitTestCase(APITestCase):

    def setUp(self):
        # Создаем пользователей
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword123'
        )
        self.other_user = User.objects.create_user(
            email='otheruser@example.com',
            password='testpassword123'
        )

        # Авторизуем основного пользователя
        self.client.force_authenticate(user=self.user)

        # Создаем публичную и приятную привычку для тестов
        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='10:00:00',
            action='Почитать книгу',
            is_pleasant=True,
            periodicity=1,
            time_to_complete=60,
            is_public=True
        )

        self.habit = Habit.objects.create(
            user=self.user,
            place='Зал',
            time='18:00:00',
            action='Тренировка',
            is_pleasant=False,
            reward='Просмотр кино',
            periodicity=1,
            time_to_complete=120,
            is_public=True
        )

    def test_habit_create(self):
        """Тест создания привычки."""
        url = reverse('habits:habit-create')
        data = {
            "place": "Парк",
            "time": "08:00:00",
            "action": "Пробежка",
            "is_pleasant": False,
            "periodicity": 1,
            "reward": "Кофе",
            "time_to_complete": 90,
            "is_public": True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 3)

    def test_habit_list(self):
        """Тест получения списка привычек текущего пользователя."""
        url = reverse('habits:habit-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_public_habit_list(self):
        """Тест получения списка публичных привычек."""
        url = reverse('habits:public-habit-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) >= 1)

    def test_habit_validation_execution_time(self):
        """Тест валидатора: время выполнения не более 120 секунд."""
        url = reverse('habits:habit-create')
        data = {
            "place": "Дом",
            "time": "08:00:00",
            "action": "Долгая медитация",
            "is_pleasant": False,
            "periodicity": 1,
            "time_to_complete": 180,  # Превышает 120 секунд
            "is_public": True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_habit_validation_periodicity(self):
        """Тест валидатора: периодичность не более 7 дней."""
        url = reverse('habits:habit-create')
        data = {
            "place": "Дом",
            "time": "08:00:00",
            "action": "Уборка",
            "is_pleasant": False,
            "periodicity": 10,  # Реже 1 раза в 7 дней
            "time_to_complete": 60,
            "is_public": True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_other_user_habit_access(self):
        """Тест запрета доступа чужому пользователю к редактированию."""
        self.client.force_authenticate(user=self.other_user)
        url = reverse('habits:habit-update', args=[self.habit.id])
        data = {"place": "Другое место"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
