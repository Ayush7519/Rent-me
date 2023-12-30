from django.shortcuts import render
from rest_framework import generics,status,permissions
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from hostel.serializer import Hostel_Serializer,HostelList_Serializer
from .models import Hostel
from rnt.pagination import MyPageNumberPagination

#creating the view for the hostel create.
class Hostel_CreateAPIVIEW(generics.CreateAPIView):
    queryset=Hostel.objects.all()
    serializer_class=Hostel_Serializer
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer=Hostel_Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            numberofseatavl=serializer.validated_data['no_of_beds']
            print(numberofseatavl)
            serializer.validated_data['no_of_bed_availabe']=numberofseatavl
            user=request.user
            serializer.validated_data['owner']=user
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

#creating the view for the hostel (admin).
class HostelList_APIVIEW(generics.ListAPIView):
    queryset=Hostel.objects.all()
    serializer_class=HostelList_Serializer
    pagination_class = MyPageNumberPagination
    permission_classes = [permissions.IsAdminUser]


#creating the view for the hostel based on approved and not approved (user).
class HostelListBased_APIVIEW(generics.ListAPIView):
    serializer_class=HostelList_Serializer

    def get_queryset(self):
        heading=self.kwargs["name"]
        if heading == "ap":
            return Hostel.objects.filter(approved=True)
        elif heading == "uap":
            return Hostel.objects.filter(approved=False)
        
    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset()
        if queryset.exists():
            serializer=self.get_serializer(queryset,many=True)
            return Response(serializer.data,)
        else:
            return Response({"msg":"Sorry we dont have any hostel approved by the admin"},
                    status=status.HTTP_404_NOT_FOUND,
            )