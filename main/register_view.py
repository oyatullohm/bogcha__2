from django.shortcuts import render , redirect
from django.contrib.auth import  login ,logout, authenticate
from django.views import View
from .models import *
from django.contrib import messages
from .help import CheckUserData
import random
class Register_chief_View(View,CheckUserData):
    def get(self,request):
        return render(request, 'account/signup.html')
    def create_token_id(self):
        return "".join(random.sample([str(num) for num in range(0,10) ], 10))
    def post(self, request):
        if self.check_data(request):
            return render(request, "account/signup.html")
        user = self.create_user(request)
        phone = request.POST['phone']
        try:
            create_token_id = self.create_token_id()
            client =  Client.objects.create(user=user,chief= True, name = user.username,phone=phone,token_id=create_token_id)
            if client:
                Month.objects.create(chief=client,)
                return redirect('main:home_admin')
        except:
            messages.add_message(request,messages.WARNING, "hatolik yuz berdi  iltmos  qytadan urinin ")
            return redirect('main:home')


class Register_educator_View(View,CheckUserData):
    def get(self,request):
        return render(request, 'account/register.html')
    def post(self,request):
        if self.check_data(request):
            return render(request, "account/signup.html")
        user = self.create_user(request)
        phone = request.POST['phone']
        token  = request.POST['token']
        chief = Client.objects.get(token_id=token)
        educator= Client.objects.create(user=user,name = user.username,phone=phone,token_code=chief.token_id)
        educator
        if educator:
            Month.objects.create(educator=educator)
            return redirect('main:home')
        messages.add_message(request,messages.WARNING, "hatolik yuz berdi  iltmos  qytadan urinin ")
        return redirect('main:signup_educator')



class LoginView(View):
    def get(self,request):
        if  request.user.is_authenticated == True:
            return redirect('main:home')
        return render (request,'account/login.html')
    def post(self,request):
        if  request.user.is_authenticated == True:
            return redirect('main:home')
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(request,username=username,password=password)
            try:
                if user is not None:
                    login(request,user)
                    return redirect('main:home')
            except:
                messages.error(request, " Логин Йоки  Парол Хато !")
                return redirect('main:login')
        return redirect('main:login')


def logout_(request):
    logout(request)
    return redirect('/')
