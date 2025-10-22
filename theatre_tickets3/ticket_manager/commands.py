# ticket_manager/commands.py
class Command:
    def execute(self):
        raise NotImplementedError


class BookTicketCommand(Command):
    def __init__(self, booking_service, user, performance, seat):
        self.booking_service = booking_service
        self.user = user
        self.performance = performance
        self.seat = seat

    def execute(self):
        return self.booking_service.book_ticket(self.user, self.performance, self.seat)


class PayTicketCommand(Command):
    def __init__(self, payment_service, booking):
        self.payment_service = payment_service
        self.booking = booking

    def execute(self):
        return self.payment_service.pay(self.booking)
