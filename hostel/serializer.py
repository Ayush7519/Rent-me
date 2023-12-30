from rest_framework import serializers
from .models import Hostel

#creating the serializer for the hostel create.
class Hostel_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Hostel
        fields="__all__"

#creating the serializer for the hostel list.
class HostelList_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Hostel
        fields="__all__"
        # depth=1

