from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.shortcuts import redirect
from .models import *

class CheckUserData:
    error = None
    def check_data(self,request):
        username = request.POST['username']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        if len(username) < 8 and  len(password) < 8:
            messages.add_message(request,messages.WARNING, "Username va parol 8 ta belgidan kam bo'lmasin")
            self.error = True
            return self.error
        if User.objects.filter(username=username).exists():
            messages.add_message(request,messages.WARNING, "Username band")
            self.error = True
            return self.error
        if password != password_confirm:
            messages.add_message(request,messages.WARNING, "Parollar bir xil emas")
            self.error = True
        return self.error

    def create_user(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username,password=password)
        user = authenticate(request,username=username, password=password)
        if user :
            login(request,user)
        return user


