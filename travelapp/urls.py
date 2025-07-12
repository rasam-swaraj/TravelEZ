from django.contrib import admin
from django.urls import path
from . import views
from .views import *

urlpatterns = [
     path('',views.Index,name="IndexPage"),
     path('index', views.PakageList,name="ListPackage"),
     path('details/<slug:slug>',views.Details,name="Details"),
     path('package-details/<slug:slug>', views.PackageDetails,name="ViewPackage"),
     path('search', views.SearchBox, name="Search"),
     path('signup', views.Signup,name="SignUp"),
     path('login', views.Login,name="LogIn"),
     path('logout', views.Logout,name="LogOut"),
     path('booking', views.BookingInfo,name="Bookings"),
     path('view/<int:id>',views.ViewPassenger,name="ViewPassenger"),
     path('kyp', views.PassengerInfo,name="PassengerInfo"),
     path('show', views.Show,name="Show"),
     path('delete/<int:id>',views.DeletePassenger,name="DeletePassenger"),
     path('edit/<int:id>',views.EditPassenger,name="Edit"),
     path('update/<int:id>', views.UpdateInfo,name="Update"),
     path('billing', views.Proceed,name="Proceed"),
     path('payment',views.PaymentView,name="Payment")
]