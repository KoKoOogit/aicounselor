from django.contrib import admin
from django.urls import path
from . import views
app_label = "main"
urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('dashboard', views.dashboard, name="dashbopard"),
    path('logout', views.logout, name="logout"),
    path('scheduler', views.scheduler, name="scheduler"),
    path('chad', views.chad, name="chad"),
    path('essay', views.essay, name="essay"),
    path('tutor', views.tutor, name="tutor"),
    path('checklist', views.checklist, name="checklist"),
]
