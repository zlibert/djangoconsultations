from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutPage, name='logout'),
    path('profile', views.profilePage, name='profile'),
    path('change/', views.changePage, name='change'),      # Update Form
    path('register', views.registerPage, name='register')  # Register Form
]
