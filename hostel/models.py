from django.db import models
from account.models import User
from multiupload.fields import MultiFileField
from rest_framework import serializers
import os

#this is for validating the image and saving the image in seperate folder.
def category_image_dir_path(instance, filename):
    nm = instance.hostel_name
    img = instance.photo
    ext = img.name.split(".")[-1]

    # Validate image extension
    valid_extensions = ["png", "jpg", "jpeg"]
    if ext.lower() not in valid_extensions:
        raise serializers.ValidationError(
            "Extension does not match. It should be of png, jpg, jpeg"
        )

    # Define the directory path for event photos
    event_photos_directory = "Hostel Photos"

    # Construct the file path within the event photos directory
    filename = f"{nm}.{ext}"
    return os.path.join(event_photos_directory, filename)

#creating the model for the hostel.
class Hostel(models.Model):
    #this is for the multiple upload of images.size define the number of images.
    photo=models.ImageField(upload_to=category_image_dir_path,blank=False,null=False)
    photo1=models.ImageField(upload_to=category_image_dir_path,blank=False,null=False)
    photo2=models.ImageField(upload_to=category_image_dir_path,blank=False,null=False)
    hostel_name=models.CharField(max_length=200,null=False,blank=False)
    description=models.TextField(blank=True,null=True)
    address=models.CharField(max_length=100,blank=False,null=False)
    contact=models.PositiveBigIntegerField(null=False,blank=False)
    price=models.PositiveBigIntegerField(blank=False,null=False)
    no_of_rooms=models.PositiveIntegerField(default=0)
    no_of_beds=models.PositiveIntegerField(default=0,null=True,blank=True)
    rating=models.IntegerField(default=0,null=True,blank=True)
    high_recommendation=models.CharField(max_length=200, blank=True,null=True)
    date_created=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateTimeField(auto_now=True)
    no_of_bed_availabe=models.PositiveIntegerField(blank=True,null=True)
    owner=models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    approved=models.BooleanField(default=False)

    def __str__(self):
        return self.hostel_name
