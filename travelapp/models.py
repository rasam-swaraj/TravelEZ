from django.utils import timezone
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Package(models.Model):
    image = models.ImageField(upload_to="images")
    package_code = models.CharField(max_length=20)
    package_name = models.CharField(max_length=50)
    package_type = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    days = models.IntegerField()
    description = models.CharField(max_length=200)
    price = models.FloatField()
    slug = models.SlugField(default="",null=False)
    
    def get_absolute_url(self):
        return reverse("Package", kwargs={"slug": self.slug})
    
    def __str__(self):
        return self.package_name
    
    class Meta:
        db_table = "package_info"

class Client(AbstractUser):
    username = None
    is_superuser = None
    is_staff = None
    is_active = None
    user_permissions = None
    groups = None
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
       return f"{self.first_name} {self.last_name}"

    class Meta: 
        db_table = "client_info"


class Booking(models.Model):
    clientid = models.ForeignKey(Client,on_delete=models.CASCADE)
    packageid = models.ForeignKey(Package,on_delete=models.CASCADE)
    passengers = models.IntegerField()
    totalprice = models.FloatField()
    booking_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.id}"
    
    class Meta:
        db_table = 'booking_info'

class Passenger(models.Model):
    genders =[('Male','Male'),('Female','Female')]
    booking_id = models.ForeignKey(Booking,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.CharField(max_length=100,choices=genders)
    address = models.CharField(max_length=100)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    pincode = models.IntegerField()
    passport_id = models.IntegerField()
    journey_date = models.DateField()

    def __str__(self):
        return f"{self.Client.first_name} {self.Client.last_name}"

    class Meta: 
        db_table = "passanger_info"

class Payment(models.Model):
    payment_id = models.CharField(max_length=150)
    clientid = models.ForeignKey(Client, on_delete=models.CASCADE)
    booking_id = models.ForeignKey(Booking,on_delete=models.CASCADE)
    amount_paid = models.CharField(max_length=150)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self) :
        return f"{self.Client.first_name}-{self.payment_id}-{self.booking_id}"

    class Meta:
        db_table = 'payment_info'


