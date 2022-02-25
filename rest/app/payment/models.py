from django.db import models
from rest.app.user.models import User
import uuid

# Create your models here.
class Transaction(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target_user = models.CharField(max_length=255, null=True, default='')
    amount = models.IntegerField()
    balance_before = models.IntegerField()
    balance_after = models.IntegerField()
    remarks = models.TextField()
    transaction_type =  models.CharField(max_length=255, null=True, default='')
    payment_type =  models.CharField(max_length=255, null=True, default='')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def get_all_transactions(self, usr):
        user = User.objects.get(phone_number=usr)

        transaction = Transaction.objects.filter(user_id = user.id)
        return transaction

    def create_topup(self, amount, usr):
        if not amount:
            raise ValueError('Transaction must have amount integer')

        user = User.objects.get(phone_number=usr)
        balance_before = user.balance
        balance_after = user.balance + int(amount)
        user.balance = balance_after
        user.save()

        transaction = Transaction(
            amount=amount,
            user_id = user.id,
            balance_before=balance_before,
            balance_after=balance_after,
            transaction_type='topup',
            payment_type='DEBIT',
            remarks=''
        )
        transaction.save()

        return transaction

    def create_payment(self, amount, remarks, usr):
        if not amount:
            raise ValueError('Transaction must have amount integer')

        user = User.objects.get(phone_number=usr)
        balance_before = user.balance
        balance_after = user.balance - int(amount)

        if balance_after<0:
            raise ValueError('Balance is not enough')

        user.balance = balance_after
        user.save()

        transaction = Transaction(
            amount=amount,
            user_id = user.id,
            balance_before=balance_before,
            balance_after=balance_after,
            transaction_type='pay',
            payment_type='CREDIT',
            remarks=remarks
        )
        transaction.save()

        return transaction

    def create_transfer(self, amount, remarks, target, usr):
        if not amount:
            raise ValueError('Transaction must have amount integer')

        user = User.objects.get(phone_number=usr)
        balance_before = user.balance
        balance_after = user.balance - int(amount)

        if balance_after<0:
            raise ValueError('Balance is not enough')

        user2 = User.objects.get(phone_number=usr)
        balance_after_user2 = user2.balance + int(amount)

        user.balance = balance_after
        user2.balance = balance_after_user2
        user.save()
        user2.save()

        transaction = Transaction(
            amount=amount,
            user_id = user.id,
            balance_before=balance_before,
            balance_after=balance_after,
            transaction_type='transfer',
            payment_type='CREDIT',
            remarks=remarks,
            target_user=target_user
        )
        transaction.save()

        return transaction

    class Meta:
        '''
        to set table name in database
        '''
        db_table = "transaction"

