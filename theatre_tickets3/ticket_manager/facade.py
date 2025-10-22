from .commands import BookTicketCommand, PayTicketCommand
from .observers import BookingSubject, EmailNotifier, AdminNotifier

class TheatreBookingFacade:
    """
    Фасад объединяет основные шаги бронирования:
    1. Создать бронь
    2. Оплатить билет
    3. Уведомить наблюдателей
    """

    def __init__(self, booking_service, payment_service):
        self.booking_service = booking_service
        self.payment_service = payment_service
        self.subject = BookingSubject()
        self.subject.attach(EmailNotifier())
        self.subject.attach(AdminNotifier())

    def book_and_pay(self, user, performance, seat):
        # 1. Бронирование
        book_cmd = BookTicketCommand(self.booking_service, user, performance, seat)
        booking = book_cmd.execute()

        # 2. Оплата
        pay_cmd = PayTicketCommand(self.payment_service, booking)
        payment_result = pay_cmd.execute()

        # 3. Уведомления
        self.subject.notify(f"Пользователь {user.username} успешно забронировал и оплатил билет.")

        return {
            "booking": booking,
            "payment": payment_result,
        }
