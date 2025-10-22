from django.urls import path
from django.contrib.auth import views as auth_views
from . import views, views_auth

urlpatterns = [
    path('', views.home, name='home'),
    path('performances/', views.performance_list, name='performance_list'),
    path('performance/<int:performance_id>/seats/', views.select_seat, name='select_seat'),
    path('book/<int:ticket_id>/', views.book_ticket, name='book_ticket'),

    # --- 🔐 Авторизация и регистрация ---
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("register/", views_auth.register, name="register"),  # ← вот эта строка обязательна
]
