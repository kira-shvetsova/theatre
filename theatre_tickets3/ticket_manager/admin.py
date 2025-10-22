from django.contrib import admin
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Performance, Seat, Ticket


class PerformanceForm(forms.ModelForm):
    class Meta:
        model = Performance
        fields = '__all__'
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'duration': forms.DurationField(),
        }


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    form = PerformanceForm
    list_display = ['title', 'date_time', 'base_price', 'formatted_duration']

    def formatted_duration(self, obj):
        if obj.duration:
            total_seconds = int(obj.duration.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            return f"{hours} ч {minutes} мин"
        return "-"

    formatted_duration.short_description = _('Продолжительность')


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['row', 'number', 'category', 'price_coefficient']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['performance', 'seat', 'status', 'final_price']
    list_filter = ['status', 'performance']
    readonly_fields = ['final_price']


# Перевод админки
admin.site.site_header = _('Администрирование Театральной кассы')
admin.site.site_title = _('Театральная касса')
admin.site.index_title = _('Управление данными')
