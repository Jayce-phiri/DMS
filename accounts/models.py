from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=12)

    # National ID validation
    national_id_validator = RegexValidator(regex=r'^\d{6}/\d{2}/\d{1}$',message="National ID must be in format XXXXXX/XX/X (digits only)")
    national_id = models.CharField(max_length=15,unique=True,validators=[national_id_validator])
    
    @property
    def full_name(self):
        return self.first_name + " " + self.last_name