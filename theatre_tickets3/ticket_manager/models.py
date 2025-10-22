from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .strategies import RegularPricing

class Performance(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    date_time = models.DateTimeField(verbose_name="Дата и время")
    duration = models.DurationField(verbose_name="Продолжительность")
    base_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Базовая цена")

    def __str__(self):
        return f"{self.title} ({self.date_time})"

    @property
    def duration_hours(self):
        """Возвращает часы продолжительности"""
        if self.duration:
            return int(self.duration.total_seconds() // 3600)
        return 0

    @property
    def duration_minutes(self):
        """Возвращает минуты продолжительности"""
        if self.duration:
            return int((self.duration.total_seconds() % 3600) // 60)
        return 0

    def create_tickets_for_all_seats(self):
        """Создает билеты для всех мест в зале для этого спектакля"""
        all_seats = Seat.objects.all()

        # Удаляем старые билеты (если есть)
        Ticket.objects.filter(performance=self).delete()

        # Создаем билеты для каждого места
        tickets_to_create = []
        for seat in all_seats:
            tickets_to_create.append(
                Ticket(performance=self, seat=seat)
            )

        # Массовое создание для эффективности
        Ticket.objects.bulk_create(tickets_to_create)
        return f"Создано {len(tickets_to_create)} билетов"


class Seat(models.Model):
    CATEGORY_CHOICES = [
        ('PARTERRE', 'Партер'),
        ('BALCONY', 'Балкон'),
        ('LOGE', 'Ложа'),
    ]
    row = models.PositiveIntegerField(verbose_name="Ряд")
    number = models.PositiveIntegerField(verbose_name="Номер")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="Категория")
    price_coefficient = models.DecimalField(max_digits=3, decimal_places=2, verbose_name="Коэффициент цены")

    class Meta:
        unique_together = ('row', 'number')

    def __str__(self):
        return f"Ряд {self.row}, Место {self.number} ({self.get_category_display()})"


class Ticket(models.Model):
    STATUS_CHOICES = [
        ('FREE', 'Свободен'),
        ('BOOKED', 'Забронирован'),
        ('SOLD', 'Продан'),
    ]
    performance = models.ForeignKey(
        Performance,
        on_delete=models.CASCADE,
        verbose_name="Спектакль"
    )
    seat = models.ForeignKey(
        Seat,
        on_delete=models.CASCADE,
        verbose_name="Место"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='FREE',
        verbose_name="Статус"
    )
    reserved_until = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Забронирован до"
    )
    reserved_by = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Забронировано (ID пользователя)"
    )

    def final_price(self, strategy=None):
        strategy = strategy or RegularPricing()
        return strategy.calculate_price(float(self.performance.base_price), self.seat)

    def __str__(self):
        return f"Билет на {self.performance} - {self.seat} [{self.status}]"

    class Meta:
        unique_together = ('performance', 'seat')  # ← добавляем это!

    def __str__(self):  # ← исправляем название метода
        return f"Билет на {self.performance} - {self.seat} [{self.status}]"

    def final_price(self):
        """Рассчитывает финальную цену билета"""
        try:
            return float(self.performance.base_price) * float(self.seat.price_coefficient)
        except (TypeError, ValueError):
            return 0.0


# Сигнал для автоматического создания билетов
@receiver(post_save, sender=Performance)
def create_tickets_for_new_performance(sender, instance, created, **kwargs):
    if created:
        instance.create_tickets_for_all_seats()

class Booking(models.Model):
    show_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seat = models.CharField(max_length=10)
    paid = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Booking #{self.id}: user={self.user.username}, seat={self.seat}, paid={self.paid}"
