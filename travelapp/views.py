from django.shortcuts import render, redirect
from .models import Package, Client, Passenger, Booking, Payment
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.

def Index(request):
    domestic = Package.objects.filter(Q(package_type__icontains="domestic"))
    international = Package.objects.filter(Q(package_type__icontains="international"))
    return render(request,'index.html',{'domestic': domestic, 'international': international})

def PakageList(request):
    domestic = Package.objects.filter(Q(package_type__icontains="domestic"))
    international = Package.objects.filter(Q(package_type__icontains="international"))
    clientsession = request.session['client']
    clientobject = Client.objects.get(email = clientsession)
    return render(request,'index.html',{'domestic': domestic, 'international': international, 'sessionvalue': clientsession, 'clientobj': clientobject})
    
def Details(request,slug):
    packageobject = Package.objects.get(slug = slug)
    return render(request,'details.html',{'packageobj': packageobject})
        
def PackageDetails(request,slug):
    clientsession = request.session['client']
    clientobject = Client.objects.get(email = clientsession)
    packageobject = Package.objects.get(slug = slug)
    return render(request,'details.html',{'packageobj': packageobject,'sessionvalue':clientsession,'clientobj':clientobject})

def SearchBox(request):
    if request.method=="POST":
        search = request.POST['search_query']
        packageobject = Package.objects.filter(Q(package_name__icontains=search) | Q(location__icontains=search) | Q(country__icontains=search))
        return render(request,'search.html',{'packageobj': packageobject})

def Signup(request):
    if request.method == "POST":
        fn = request.POST.get('fname')
        ln = request.POST.get('lname')
        phoneno = request.POST.get('phno')
        email1 = request.POST.get('email')
        password = request.POST.get('pass')
        password = make_password(password)
        clientobject = Client(first_name = fn, last_name = ln, phone_number = phoneno, email = email1, password = password)

        if Client.objects.filter(email = email1):
            messages.warning(request, "Email already exists.")
        
        elif(len(fn)<3):
            messages.warning(request, "Firstname cannot be less than 3 characters.")

        else:
            messages.success(request, "User created successfully." )
            clientobject.save()

        return render(request,'signup.html')
    else:
        return render(request,'signup.html')

def Login(request):
    if request.method == "POST":
        try:
            email1 = request.POST['username']
            password1 = request.POST['pass']
            client = Client.objects.get(email=email1)
        except:
            messages.error(request,"Invalid Username")
            return render(request,"login.html")
        user = authenticate(email=email1, password=password1)
        if user is not None:
            login(request, user)
            print("loggedin")
            request.session.modified = True
            request.session['client'] = email1
            return redirect("../index")
        else:
            messages.error(request,"Incorrect Password")
            return render(request,"login.html")
    else:   
        return render(request,'login.html')

def Logout(request):
    # del request.session['client'] 
    # clientsession = ''
    logout(request)
    return redirect('../')

def BookingInfo(request):
    clientsession = request.session['client']
    clientobject = Client.objects.get(email = clientsession)
    client_id = clientobject.id
    bookingobject = Booking.objects.filter(clientid = client_id)
    return render(request,'bookings.html',{'sessionvalue':clientsession, 'bookingobj': bookingobject, 'clientobj':clientobject})

def ViewPassenger(request,id):
    clientsession = request.session['client']
    clientobject = Client.objects.get(email = clientsession)
    passengerobject = Passenger.objects.filter(booking_id = id)
    return render(request,'view.html',{'passengerobj': passengerobject, 'clientobj':clientobject})

def PassengerInfo(request):
    if request.method == "POST":
        clientsession = request.session['client']
        print(clientsession)
        package_id = request.POST['package_id']
        package_id = int(package_id)
        print(package_id)
        print(type(package_id))
        book_id = request.POST['book_id']
        print(book_id)
        print(type(book_id))
        return render(request,'kyp.html',{'package_id': package_id, 'book_id': book_id})
    

def Show(request):
    if request.method == "POST":
        clientsession = request.session['client']
        package_id = request.POST['package_id']
        package_id = int(package_id)
        book_id = request.POST['book_id']
        book_id = int(book_id)
        print(book_id)
        print(type(book_id))
        clientobject = Client.objects.get(email =  clientsession)
        packageobject = Package.objects.get(pk = package_id)
        count = 0
        totalamt = 0
        if book_id == 0:
            bookingobject = Booking(clientid = clientobject, packageid = packageobject, passengers = 1, totalprice = packageobject.price)
            bookingobject.save()
            book_id = bookingobject.id
            print(book_id)
            print(type(book_id))
        else:
            bookingobject = Booking.objects.get(clientid = clientobject.id, packageid = packageobject.id, pk = book_id)
            count = bookingobject.passengers + 1
            totalamt = packageobject.price * count
            bookingobject.passengers = count
            bookingobject.totalprice = totalamt
            bookingobject.save()

        bookingobject = Booking.objects.get(pk = book_id)
        passdata = Passenger()
        passdata.booking_id = bookingobject
        passdata.firstname = request.POST.get('firstname')
        passdata.lastname = request.POST.get('lastname')
        passdata.age = request.POST.get('age')
        passdata.gender = request.POST.get('gender')
        passdata.address = request.POST.get('address')
        passdata.country = request.POST.get('country')
        passdata.state = request.POST.get('state')
        passdata.pincode = request.POST.get('pincode')
        passdata.passport_id = request.POST.get('passport')
        passdata.journey_date = request.POST.get('dateofjourney')
        passdata.save()

        passengerobject = Passenger.objects.filter(booking_id = bookingobject.id)
        return render(request,'show.html',{'package_id':package_id, 'bookingobj':bookingobject, 'passengerobj':passengerobject, 'sessionvalue':clientsession, 'book_id': book_id})

def DeletePassenger(request,id):
    clientsession = request.session['client']
    passengerobject = Passenger.objects.get(id = id)
    book_id = passengerobject.booking_id_id
    book_id = int(book_id)
    print(book_id)
    bookingobject = Booking.objects.get(pk = book_id)
    package_id = bookingobject.packageid_id
    package_id = int(package_id)
    print(package_id)
    packageobject =Package.objects.get(pk = package_id)
    count = bookingobject.passengers - 1
    totalamt = packageobject.price * count
    bookingobject.passengers = count
    bookingobject.totalprice = totalamt
    bookingobject.save()
    passengerobject.delete()
    passengerobject = Passenger.objects.filter(booking_id = book_id)
    return render(request,'show.html',{'package_id':package_id, 'bookingobj':bookingobject, 'passengerobj':passengerobject, 'sessionvalue':clientsession, 'book_id': book_id})

def EditPassenger(request,id):
    passengerobject = Passenger.objects.get(id = id)
    return render(request,'update.html',{'passengerobj': passengerobject})

def UpdateInfo(request,id):
    if request.method == "POST":
        clientsession = request.session['client']
        passengerobject = Passenger.objects.get(id = id)
        book_id = passengerobject.booking_id_id
        book_id = int(book_id)
        bookingobject = Booking.objects.get(pk = book_id)
        package_id = bookingobject.packageid_id
        package_id = int(package_id)
        passengerobject.booking_id = bookingobject
        passengerobject.firstname = request.POST.get('firstname')
        passengerobject.lastname = request.POST.get('lastname')
        passengerobject.age = request.POST.get('age')
        passengerobject.gender = request.POST.get('gender')
        passengerobject.address = request.POST.get('address')
        passengerobject.country = request.POST.get('country')
        passengerobject.state = request.POST.get('state')
        passengerobject.pincode = request.POST.get('pincode')
        passengerobject.passport_id = request.POST.get('passport')
        passengerobject.save()
        passengerobject = Passenger.objects.filter(booking_id = book_id)
        return render(request,'show.html',{'package_id':package_id, 'bookingobj':bookingobject, 'passengerobj':passengerobject, 'sessionvalue':clientsession, 'book_id': book_id})


def Proceed(request):
    if request.method == "POST":
        clientsession = request.session['client']
        package_id = request.POST['package_id']
        package_id = int(package_id)
        book_id = request.POST['book_id']
        book_id = int(book_id)
        clientobject = Client.objects.get(email =  clientsession)
        packageobject = Package.objects.get(pk = package_id)
        bookingobject = Booking.objects.get(pk = book_id)
    return render(request,'billing.html',{'bookingobj':bookingobject, 'sessionvalue':clientsession})

def PaymentView(request):
    if request.method == "POST":
        clientsession = request.POST['user']
        tsid = request.POST['tsid']
        book_id = request.POST['book_id']
        status = request.POST['status']
        amountpaid = request.POST['amountpaid']
        clientobject = Client.objects.get(email = clientsession)
        bookingobject = Booking.objects.get(pk = book_id)
        paymentobject = Payment()
        paymentobject.payment_id = tsid
        paymentobject.amount_paid = amountpaid
        paymentobject.status = status 
        paymentobject.clientid = clientobject
        paymentobject.booking_id = bookingobject
        paymentobject.save()

        subject = 'Booking successfull'
        message = f'Hi {clientobject.firstname} {clientobject.lastname}, thank you for booking with us.\nHope you have a great experience.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['swarajrasam12@gmail.com',] 
        send_mail( subject, message, email_from, recipient_list )
    return redirect('../index')
