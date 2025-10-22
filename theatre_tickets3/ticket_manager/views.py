from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Performance, Ticket
from .facade import TheatreBookingFacade

# Простые mock-сервисы для бронирования и оплаты
class BookingService:
    def book_ticket(self, user, performance, seat):
        ticket = Ticket.objects.get(performance=performance, seat=seat)
        if ticket.status != 'FREE':
            raise Exception("Место уже занято.")
        ticket.status = 'BOOKED'
        ticket.reserved_by = user.username
        ticket.save()
        return ticket


class PaymentService:
    def pay(self, ticket):
        ticket.status = 'SOLD'
        ticket.save()
        return {"status": "success", "message": "Оплата прошла успешно"}


def home(request):
    return render(request, "home.html")


def performance_list(request):
    performances = Performance.objects.all()
    return render(request, "performance_list.html", {"performances": performances})


@login_required
def select_seat(request, performance_id):
    performance = get_object_or_404(Performance, id=performance_id)
    tickets = Ticket.objects.filter(performance=performance).select_related("seat")
    return render(request, "select_seat.html", {"performance": performance, "tickets": tickets})


@login_required
def book_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    facade = TheatreBookingFacade(BookingService(), PaymentService())

    try:
        result = facade.book_and_pay(request.user, ticket.performance, ticket.seat)
        messages.success(request, "Билет успешно забронирован и оплачен!")
    except Exception as e:
        messages.error(request, f"Ошибка: {e}")

    return redirect("performance_list")
