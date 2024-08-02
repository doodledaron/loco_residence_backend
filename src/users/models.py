
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

from users.managers import CustomUserManager, AdminManager, GuardManager, ResidentManager, SuperAdminManager



#phone validator
phone_regex = RegexValidator(regex=r'^01\d{8,9}$', message="Phone number entered in the wrong format. Only Malaysian phone number is allowed")

#Here is where we set our user models
class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        SUPER_ADMIN = 'super_admin', 'Super Admin'
        ADMIN = 'admin', 'Admin'
        GUARD = 'guard', 'Guard'
        RESIDENT = 'resident', 'Resident'
        
    base_role = Role.SUPER_ADMIN
    role = models.CharField(max_length=50, choices=Role.choices, default=base_role)
    
    objects = CustomUserManager()
    
    username = None #username is not we wanted as the identifier
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email" #defines the unique identifier for the User model -- to email
    REQUIRED_FIELDS = ['first_name', 'last_name'] #list of field names that will be prompted when creating a superuser -> meaning Django will prompt for email,password,first name and last name
    
    full_name = models.CharField(max_length=180)
    phone_number = models.CharField(validators=[phone_regex], max_length=11, blank=True) # Validators should be a list
    
    #full name = last name + first name while saving
    def save(self, *args, **kwargs):
        #if user doesnt exists
        if not self.pk:
            self.role = self.base_role
            self.full_name = f"{self.last_name} {self.first_name}"
            self.email = self.email.lower()
            return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"User email: {self.email}"
    





        
class SuperAdmin(CustomUser):
    base_role = CustomUser.Role.SUPER_ADMIN
    objects = SuperAdminManager()
    
    class Meta:
        proxy = True
        
class Admin(CustomUser):
    base_role = CustomUser.Role.ADMIN
    objects = AdminManager()
    
    class Meta:
        proxy = True
        
class Guard(CustomUser):
    base_role = CustomUser.Role.GUARD
    objects = GuardManager()
    
    class Meta:
        proxy = True
        
class Resident(CustomUser):
    base_role = CustomUser.Role.RESIDENT
    objects = ResidentManager()
    
    #Proxy models allow you to change the behavior of the original model without altering its schema
    #This means that the Resident class does not create a new database table; instead, it uses the existing table of the CustomUser model.
    class Meta:
        proxy = True
        
class Feedback(models.Model):
    resident_id = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name='resident_feedback')
    description = models.TextField()
    rating = models.IntegerField()
    feedback_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Feedback from {self.resident_id}"
