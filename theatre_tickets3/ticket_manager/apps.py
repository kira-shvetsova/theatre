from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class TicketManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ticket_manager'
    verbose_name = _('Управление билетами')
