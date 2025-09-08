from django.urls import path
from . import views

urlpatterns = [
    path('send/card/', views.send_card_transaction, name='send-card-transaction'),
    path('send/ach/', views.send_ach_transaction, name='send-ach-transaction'),
]
