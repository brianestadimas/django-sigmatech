from django.conf.urls import url
from rest.app.payment.views import TopupView, PayView, TransferView, TransactionView


urlpatterns = [
    url(r'^topup', TopupView.as_view()),
    url(r'^pay', PayView.as_view()),
    url(r'^transfer', TransferView.as_view()),
    url(r'^transactions', TransactionView.as_view()),
]
