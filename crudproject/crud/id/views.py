from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView, View
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import redirect
# import pymysql
from django.contrib import messages
from id.models import Person
import json
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView


# Create your views here.
def login_page(request):
    return render(request, 'id/login.html')


def welcome_page(request):
    return render(request, 'id/welcome.html')


def index(request):
    return render(request, 'id/home.html', context={})


def form_data(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        Company_name = request.POST['company']
        Email_name = request.POST['Email']
        Phone_number = request.POST['Phone']
        Password = make_password(request.POST['Password'])
        if Person.objects.filter(Phone_number=Phone_number).exists():
            messages.error(request, "phone number already exists")
            return redirect('/')

        elif Person.objects.filter(Email_name=Email_name).exists():
            messages.error(request, "Email id already exists")
            return redirect('/')

        else:
            Person.objects.create(first_name=first_name,
                                  last_name=last_name, Company_name=Company_name,
                                  Email_name=Email_name, Phone_number=Phone_number, Password=Password)
            return redirect('/login/')

def Login_form(request):
    if request.method == 'POST':
        Phone_number = request.POST['Phone']
        User_Password = request.POST['Password']
        if Person.objects.filter(Phone_number=Phone_number).exists():
            obj = Person.objects.get(Phone_number=Phone_number)
            Password = obj.Password
            if check_password(User_Password, Password):
                return redirect('/welcome/')
            else:
                return HttpResponse('password incorrect')
        else:
            return HttpResponse('phone number is not registered')

def data(request):
    persons = Person.objects.filter(is_active=True).order_by('id')

    return render(request, 'id/table.html', context={
        'request': request,
        'persons': persons,
    })

def delete_user(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        uid = json.loads(data)
        if Person.objects.filter(id=uid).exists():
            Person.objects.filter(id=uid).update(is_active=False)
            return JsonResponse({"staus": True, "message": "User has been deleted"})
        else:
            return JsonResponse({"staus": False, "message": "User not exists."})
    else:
        return JsonResponse({"staus": False, "message": "Method not allowed."})
    
def update_view(request, uid):
    res = Person.objects.get(id=uid)
    return render(request, 'id/update.html', context={

        'person': res,
    })

def update_form_data(request):
    if request.method == 'POST':
        uid = request.POST['uid']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        Company_name = request.POST['company']
        Email_name = request.POST['Email']
        Phone_number = request.POST['Phone']

        Person.objects.filter(id=uid).update(first_name=first_name,
                                             last_name=last_name, Company_name=Company_name,
                                             Email_name=Email_name, Phone_number=Phone_number)
        return redirect('/data/')
# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

    
