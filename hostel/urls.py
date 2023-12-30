from django.urls import path
from . import views

urlpatterns = [
    path("hostel/create/",views.Hostel_CreateAPIVIEW.as_view(),name="path to create the hostel details."),
    path("hostel/adlist/",views.HostelList_APIVIEW.as_view(),name="path to see the list of hostel for the admin"),
    path("hostel/list/<str:name>/",views.HostelListBased_APIVIEW.as_view(),name="path to get the hostel list based on approved for the users."),

]