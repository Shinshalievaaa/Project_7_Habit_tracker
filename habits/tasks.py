from django.utils import timezone
from celery import shared_task
from habits.models import Habit
from habits.services import send_telegram_message


@shared_task
def send_habit_reminders():
    """Фоновая задача с учетом локального часового пояса."""
    # timezone.now() возвращает текущее дата-время с учетом TIME_ZONE из settings.py
    now = timezone.localtime(timezone.now())
    current_hour = now.hour
    current_minute = now.minute

    # Поиск привычек, запланированных на текущую минуту локального времени
    habits = Habit.objects.filter(
        time__hour=current_hour,
        time__minute=current_minute
    ).select_related('user')

    print(f"[DEBUG] Поиск привычек на {current_hour:02d}:{current_minute:02d}. Найдено: {habits.count()}")

    for habit in habits:
        user = habit.user
        if user and user.tg_chat_id:
            message = (
                f"⏰ Напоминание о привычке!\n\n"
                f"📌 Действие: {habit.action}\n"
                f"📍 Место: {habit.place}\n"
                f"⏱ Время на выполнение: {habit.time_to_complete} сек."
            )
            if habit.reward:
                message += f"\n🎁 Вознаграждение: {habit.reward}"
            elif habit.related_habit:
                message += f"\n😊 Приятная привычка: {habit.related_habit.action}"

            send_telegram_message(user.tg_chat_id, message)
