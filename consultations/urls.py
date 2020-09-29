from django.urls import path

from . import views

app_name = 'consultations'
urlpatterns = [
    # /consultations/
    path('', views.index, name='index'),
    path('<int:consultation_id>/', views.detail, name= 'detail'),
    path('add/', views.add, name= 'add'),                        # Add Form
    path('change/<int:consultation_id>/', views.change, name= 'change'),                # Update Form
    path('pricing/', views.pricing, name= 'pricing'),
    path('faq/', views.faq, name= 'faq'),
    path('terms/', views.terms, name= 'terms'),
    path('contact/', views.contact, name= 'contact')
]