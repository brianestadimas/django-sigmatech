import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    '''
    creating a manager for a custom user model
    https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#writing-a-manager-for-a-custom-user-model
    '''
    def create_user(self, phone_number, first_name, last_name=None, address=None, pin=None):
        if not phone_number:
            raise ValueError('Users Must Have a phone_number')

        user = self.model(
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            address=address
        )
        user.pin = pin
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    id = models.AutoField(primary_key=True)
    phone_number = models.CharField(max_length=255, unique=True, blank=True)
    pin = models.CharField(max_length=10, unique=False, null=False, default='', blank=True)
    password = models.UUIDField(default=uuid.uuid4)
    first_name = models.CharField(max_length=255, null=False, blank=True, default='')
    last_name = models.CharField(max_length=255, null=True, default='')
    address = models.CharField(max_length=1024, null=True, default='')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    balance = models.IntegerField(default=0, null=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['pin', 'first_name']

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        return self.phone_number

    class Meta:
        '''
        to set table name in database
        '''
        db_table = "user"
