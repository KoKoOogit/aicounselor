from django.contrib import admin
from django.urls import path
from . import views
app_label = "main"
urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('dashboard', views.dashboard, name="dashbopard"),
    path('logout', views.logout, name="logout")
]
