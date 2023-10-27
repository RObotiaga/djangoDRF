from django.core.management.base import BaseCommand
from courses.models import Payment  # Замените 'yourapp' на имя вашего приложения
from datetime import datetime
from decimal import Decimal
import random
class Command(BaseCommand):
    help = 'Кастомная команда для записи данных в модель Payment'

    def handle(self, *args, **kwargs):
        # Генерируем 5 записей в модели Payment
        for _ in range(5):
            Payment.objects.create(
                user_id=1,
                payment_date=datetime.now(),
                course_id=None,
                lesson_id=None,
                amount=Decimal(random.uniform(10.0, 100.0)).quantize(Decimal('0.01')),
                payment_method=random.choice(['cash', 'transfer'])
            )

        self.stdout.write(self.style.SUCCESS('Сгенерированы 5 записей в модели Payment.'))
