
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.core.validators import RegexValidator

#phone validator
phone_regex = RegexValidator(regex=r'^01\d{8,9}$', message="Phone number entered in the wrong format. Only Malaysian phone number is allowed")

#Here is where we set our user models
class CustomUser(AbstractUser):
    username = None #username is not we wanted as the identifier
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email" #defines the unique identifier for the User model -- to email
    REQUIRED_FIELDS = ['first_name', 'last_name'] #list of field names that will be prompted when creating a superuser -> meaning Django will prompt for email,password,first name and last name
    
    objects = CustomUserManager()

    full_name = models.CharField(max_length=180, editable=False)
    phone_number = models.CharField(validators=[phone_regex], max_length=11, blank=True) # Validators should be a list
    
    #full name = last name + first name while saving
    def save(self, *args, **kwargs):
        self.full_name = f"{self.last_name} {self.first_name}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.email