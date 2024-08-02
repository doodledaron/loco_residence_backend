from django.contrib.auth.base_user import BaseUserManager

#manager for CustomUser
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class SuperAdminManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        from users.models import CustomUser
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=CustomUser.Role.SUPER_ADMIN)

class AdminManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        from users.models import CustomUser
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=CustomUser.Role.ADMIN)
    
class GuardManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        from users.models import CustomUser
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=CustomUser.Role.GUARD)

class ResidentManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        from users.models import CustomUser
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=CustomUser.Role.RESIDENT)
    