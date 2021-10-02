from django.contrib.auth.models import BaseUserManager

# Manger for User model
class MyUserManager(BaseUserManager):
    def create_user(self, email, password, first_name, last_name, department, semester, is_staff, is_superuser):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            department=department,
            semester=semester,
            is_staff = is_staff,
            is_superuser = is_superuser,
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, first_name, last_name, department, semester):
        user = self.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            department=department,
            semester=semester,
            is_staff=True,
            is_superuser=True
        )
        return user