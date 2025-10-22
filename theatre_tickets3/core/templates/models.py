from django.db import models
from django.contrib.auth.models import User

# Расширяем стандартную модель пользователя (опционально)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Здесь можно добавить дополнительные поля: телефон, дата рождения и т.д.

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Ожидает оплаты'),
        ('PAID', 'Оплачен'),
        ('CANCELLED', 'Отменен'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    # В реальной системе это была бы ссылка на билеты в МП2. Здесь храним как текст.
    tickets_info = models.TextField(verbose_name="Информация о билетах (ID билетов)")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая сумма")
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING', verbose_name="Статус")

    def __str__(self):
        return f"Заказ #{self.id} от {self.user.username}"
