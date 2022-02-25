from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest.app.user.serializers import UserRegistrationSerializer
from rest.app.payment.models import Transaction
from rest.app.user.models import User
from rest.app.user.serializers import UserSerializer, TopupSerializer, PaySerializer, TransferSerializer, TransactionSerializer
from rest_framework import status
import datetime as dt
import pytz
import json
from django.core.serializers.json import DjangoJSONEncoder

class ProfileView(APIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        serializer = UserSerializer(request.user)
        status_code = status.HTTP_200_OK
        return Response(serializer.data, status=status_code)


class TopupView(APIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def post(self, request):
        new_transaction = Transaction().create_topup(amount=request.data.get('amount', None), usr=request.user)

        event_date = dt.datetime.now().replace(tzinfo=pytz.UTC)
        local_date = event_date.astimezone(pytz.timezone('Asia/Jakarta'))
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'Successfully Topup',
            'result': TopupSerializer(new_transaction).data,
            'created_at': local_date.strftime('%m/%d/%Y %H:%M:%S %Z')
        }
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)


class PayView(APIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def post(self, request):
        new_transaction = Transaction().create_payment(amount=request.data.get('amount', None), 
            remarks=request.data.get('remarks', None), usr=request.user)

        event_date = dt.datetime.now().replace(tzinfo=pytz.UTC)
        local_date = event_date.astimezone(pytz.timezone('Asia/Jakarta'))
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'Successfully Pay',
            'result': PaySerializer(new_transaction).data,
            'created_at': local_date.strftime('%m/%d/%Y %H:%M:%S %Z')
        }
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)


class TransferView(APIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def post(self, request):
        new_transaction = Transaction().create_payment(amount=request.data.get('amount', None), 
            remarks=request.data.get('remarks', None), target=request.data.get('target_user', None), usr=request.user)

        event_date = dt.datetime.now().replace(tzinfo=pytz.UTC)
        local_date = event_date.astimezone(pytz.timezone('Asia/Jakarta'))
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'Successfully Transfer',
            'result': TransferSerializer(new_transaction).data,
            'created_at': local_date.strftime('%m/%d/%Y %H:%M:%S %Z')
        }
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)


class TransactionView(APIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        all_transactions = Transaction().get_all_transactions(usr=request.user)
        transaction = []
        for trx in all_transactions:
            transaction.append(TransactionSerializer(trx).data)

        event_date = dt.datetime.now().replace(tzinfo=pytz.UTC)
        local_date = event_date.astimezone(pytz.timezone('Asia/Jakarta'))
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'result': transaction,
            'created_at': local_date.strftime('%m/%d/%Y %H:%M:%S %Z')
        }
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)