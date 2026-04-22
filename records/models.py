from datetime import date,timezone
import random
from django.utils import timezone
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
    

class Certifiers(models.Model):
    deceased = models.OneToOneField(Deceased, on_delete=models.CASCADE, related_name='certifiers')
    certifier = models.ForeignKey(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=50, unique=True)
    license_expiry_date = models.DateField()
    date_certified = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.certifier.username} certified the Death of {self.deceased.title_and_name} on {self.date_certified}"
    

class DeathCertificate(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING"
        APPROVED = "APPROVED"
        REJECTED = "REJECTED"

    deceased = models.OneToOneField(Deceased, on_delete=models.CASCADE, related_name='death_certificate')
    certifier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='issued_certificates')
    certificate_number = models.CharField(max_length=50, unique=True, editable=False)
    date_of_death = models.DateField()
    other_findings = models.TextField(blank=True, null=True)
    place_of_death = models.CharField(max_length=200)
    cause_of_death = models.CharField(max_length=500)
    date_issued = models.DateField(default=date.today)
    status = models.CharField(max_length=20,choices=Status.choices,default=Status.PENDING)
    date_registered = models.DateTimeField(auto_now_add=True)

    def generate_certificate_number(self):
        timestamp = timezone.now().strftime("%y%m%d%H%M%S")
        random_digits = str(random.randint(100, 999))
        return f"{timestamp}{random_digits}"

    def save(self, *args, **kwargs):
        if not self.certificate_number:
            self.certificate_number = self.generate_certificate_number()

            # Ensure uniqueness (rare collision safety)
            while DeathCertificate.objects.filter(
                certificate_number=self.certificate_number
            ).exists():
                self.certificate_number = self.generate_certificate_number()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Death Certificate No#{self.certificate_number} for {self.deceased.title_and_name}"
    
class NextOfKin(models.Model):
    class Relationship(models.TextChoices):
        SPOUSE = "Spouse", "Spouse"
        CHILD = "Child", "Child"
        PARENT = "Parent", "Parent"
        SIBLING = "Sibling", "Sibling"
        OTHER = "Other", "Other"
    deceased = models.ForeignKey(Deceased, on_delete=models.CASCADE, related_name='next_of_kin')
    full_name = models.CharField(max_length=200)
    relationship = models.CharField(max_length=100, choices=Relationship.choices)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.full_name} ({self.relationship}) - Next of Kin for {self.deceased.title_and_name}"
    
# class DeathRecords(models.Model):
#     deceased = models.OneToOneField(Deceased, on_delete=models.CASCADE, related_name='death_record')
#     death_certificate = models.OneToOneField(DeathCertificate, on_delete=models.CASCADE)   
#     certifier = models.OneToOneField(User, on_delete=models.CASCADE)
#     status = models.CharField(max_length=20,choices=DeathCertificate.Status.choices,default=DeathCertificate.Status.PENDING)
#     timestamp = models.DateTimeField(auto_now_add=True)
    
  
    # def __str__(self):
    #     return f"{self.deceased.full_name} - {self.status}"