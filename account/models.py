from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from rest_framework import serializers
import os
# CUSTOME USER MANAGER:
class UserManager(BaseUserManager):
    def create_user(
        self,
        email,
        name,
        username,
        phone,
        photo,
        password=None,
        password2=None,
        **extra_fields,
    ):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            username=username,
            phone=phone,
            photo=photo
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email,
        username,
        phone,
        password,
        name,
        photo,
        **extra_fields,
    ):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            name=name,
            phone=phone,
            photo=photo
        )

        user.is_admin = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

def category_image_dir_path(instance, filename):
    nm = instance.name
    img = instance.photo
    ext = img.name.split(".")[-1]

    # Validate image extension
    valid_extensions = ["png", "jpg", "jpeg"]
    if ext.lower() not in valid_extensions:
        raise serializers.ValidationError(
            "Extension does not match. It should be of png, jpg, jpeg"
        )

    # Define the directory path for event photos
    event_photos_directory = "User Photos"

    # Construct the file path within the event photos directory
    filename = f"{nm}.{ext}"
    return os.path.join(event_photos_directory, filename)

# USER MODEL
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="E-mail",
        max_length=255,
        unique=True,
    )
    photo=models.ImageField(upload_to=category_image_dir_path,blank=True,null=True)
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    phone=models.PositiveBigIntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "name","phone","photo"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def __str__(self):
        return self.name
