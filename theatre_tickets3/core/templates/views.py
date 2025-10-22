from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from ticket_manager.service import TicketManagerService
from ticket_manager.models import Performance
from .models import Order


def performance_list(request):
    """Главная страница - афиша спектаклей."""
    try:
        performances = TicketManagerService.get_available_performances()
        return render(request, 'core/performance_list.html', {'performances': performances})
    except Exception as e:
        messages.error(request, f"Ошибка при загрузке спектаклей: {str(e)}")
        return render(request, 'core/performance_list.html', {'performances': []})


def performance_detail(request, performance_id):
    """Страница спектакля с выбором мест."""
    try:
        performance = get_object_or_404(Performance, id=performance_id)
        available_tickets = TicketManagerService.get_available_tickets(performance_id)


    except Exception as e:
        messages.error(request, f"Ошибка при загрузке страницы: {str(e)}")
        return redirect('core:performance_list')


@login_required
def reserve_tickets(request):
    """Обработка бронирования билетов."""
    if request.method == 'POST':
        performance_id = request.POST.get('performance_id')
        selected_ticket_ids = request.POST.getlist('ticket_ids')

        if not selected_ticket_ids:
            messages.error(request, "Вы не выбрали ни одного места.")
            return redirect('core:performance_detail', performance_id=performance_id)

        try:
            ticket_ids = [int(tid) for tid in selected_ticket_ids]
            reserved_tickets = TicketManagerService.reserve_tickets(ticket_ids, str(request.user.id))

            total = sum(float(ticket.final_price()) for ticket in reserved_tickets)
            order = Order.objects.create(
                user=request.user,
                tickets_info=f"Билеты: {', '.join(str(t.id) for t in reserved_tickets)}",
                total_amount=total,
                status='PENDING'
            )
            request.session['current_order_id'] = order.id
            messages.success(request, f"Билеты забронированы! У вас есть 15 минут на оплату. Сумма: {total:.2f} руб.")
            return redirect('core:order_confirmation')

        except Exception as e:
            messages.error(request, f"Ошибка при бронировании: {str(e)}")
            return redirect('core:performance_detail', performance_id=performance_id)

    return redirect('core:performance_list')


@login_required
def order_confirmation(request):
    """Страница подтверждения заказа."""
    order_id = request.session.get('current_order_id')
    if not order_id:
        messages.error(request, "Заказ не найден.")
        return redirect('core:performance_list')

    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'core/order_confirmation.html', {'order': order})


@login_required
def confirm_purchase(request):
    """Подтверждение покупки."""
    if request.method == 'POST':
        order_id = request.session.get('current_order_id')
        if not order_id:
            messages.error(request, "Заказ не найден.")
            return redirect('core:performance_list')

        order = get_object_or_404(Order, id=order_id, user=request.user)

        try:
            ticket_ids_str = order.tickets_info.replace("Билеты: ", "").split(", ")
            ticket_ids = [int(tid) for tid in ticket_ids_str]

            TicketManagerService.confirm_purchase(ticket_ids)
            order.status = 'PAID'
            order.save()

            if 'current_order_id' in request.session:
                del request.session['current_order_id']

            messages.success(request, "Оплата прошла успешно! Ваши билеты готовы.")
            return redirect('core:performance_list')

        except Exception as e:
            messages.error(request, f"Ошибка при оплате: {str(e)}")
            return redirect('core:order_confirmation')

    return redirect('core:performance_list')


def custom_logout(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из системы.")
    return redirect('core:performance_list')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно!")
            return redirect('core:performance_list')
    else:
        form = UserCreationForm()

    return render(request, 'core/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('core:performance_list')


@login_required
def profile(request):
    """Личный кабинет пользователя."""
    from ticket_manager.models import Ticket

    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    booked_tickets = Ticket.objects.filter(reserved_by=str(request.user.id), status='BOOKED')
    purchased_tickets = Ticket.objects.filter(reserved_by=str(request.user.id), status='SOLD')

    return render(request, 'core/profile.html', {
        'orders': orders,
        'booked_tickets': booked_tickets,
        'purchased_tickets': purchased_tickets,
    })
