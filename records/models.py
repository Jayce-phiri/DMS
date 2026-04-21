from datetime import date
from accounts.models import User
from django_countries.fields import CountryField
from django.core.validators import RegexValidator
from django.db import models

class Deceased(models.Model):

    class Title(models.TextChoices):
        MR = "Mr.", "Mr."
        MRS = "Mrs.", "Mrs."
        MS = "Ms.", "Ms."

    class Gender(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"

    title = models.CharField(max_length=4, choices=Title.choices)
    gender = models.CharField(max_length=1, choices=Gender.choices)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    country = CountryField(blank_label="(select country)")

    national_id_validator = RegexValidator(
        regex=r'^\d{6}/\d{2}/\d{1}$',
        message="National ID must be in format XXXXXX/XX/X (digits only)"
    )
    national_id = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        unique=True,
        validators=[national_id_validator]
    )

    address = models.CharField(max_length=200, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)

    @property
    def age(self):
        if not self.date_of_birth or not self.date_of_death:
            return None

        return self.date_of_death.year - self.date_of_birth.year - (
            (self.date_of_death.month, self.date_of_death.day) <
            (self.date_of_birth.month, self.date_of_birth.day)
        )

    @property
    def title_and_name(self):
        return f"{self.title} {self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.title_and_name