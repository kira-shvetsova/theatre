from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.performance_list, name='performance_list'),
    path('performance/<int:performance_id>/', views.performance_detail, name='performance_detail'),
    path('reserve/', views.reserve_tickets, name='reserve_tickets'),
    path('order/', views.order_confirmation, name='order_confirmation'),
    path('confirm_purchase/', views.confirm_purchase, name='confirm_purchase'),
    path('logout/', views.custom_logout, name='logout'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]
