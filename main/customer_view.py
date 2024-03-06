from django.shortcuts import render , redirect
from django.views import View
from .models import *
from django.contrib import messages
from .help import CheckUserData
from .decorator import  user_chief , user_educator

class Customer_updateView(View):
    @user_chief
    def post(self,request,id):
        name = request.POST.get('name')
        name = name.replace("о","o")
        phone = request.POST.get('phone')
        phone = phone.replace("о","o")
        vznos = request.POST.get('vznos')
        active = request.POST.get('active')
        day_summa = request.POST.get('day_summa')
        educator = request.POST.get('educator')
        educator = Client.objects.get(id=int(educator))
        customer = Customer.objects.get(id=int(id))
        if day_summa == 'on':
            customer.day_summa =  True
        else:
            customer.day_summa = False
        if active == 'on':
            customer.active =  True
        else:
            customer.active = False
        customer.educator = educator
        customer.name = name
        customer.phone = phone
        if customer.total_summa != vznos:
            customer.total_summa = vznos
            month =  customer.months_customers.all().order_by('-id')[0]
            month.total_summa =  vznos
            month.save()
        customer.save()
        messages.success(request, " Тахрирлаш  Амалга ошди ")
        return redirect(f'/customer/admin/{id}')


class DetailCustomerView(View):
    @user_chief
    def get(self,request,pk):
        user = request.user.user
        month_chief = Month.objects.filter(chief=user).order_by('-id')[0]
        customer = Customer.objects.get(id=int(pk))
        month = Month.objects.filter(customer=customer).order_by('-id')
        educator = Client.objects.filter(token_code  =  user.token_id)
        context = {'month':month,'customer':customer , 'educator': educator}
        return render(request,'customer/customer.html',context)
    @user_chief
    def post(self,request,pk):
        summa = request.POST.get('summa')
        month = request.POST.get('month')
        user = request.user.user
        customer = Customer.objects.get(id =int(pk))
        educator = customer.educator
        month = Month.objects.get(id=int(month))
        month.summa+=int(summa)
        month.save()
        month_chief = Month.objects.filter(chief=user).order_by('-id')[0]
        month_chief.total_summa += int(summa)
        month_chief.save()
        user.balans_summa += int(summa)
        user.save()
        Payment.objects.create(user=user.user  , chief_user=user , educator=educator , customer = customer , summa = int(summa))
        messages.success(request, " Тулов  Амалга ошди ")
        return redirect(f'/customer/admin/{pk}')

class Customer_month_DetailView(View):
    @user_chief
    def get(self,request,id):
        month = Month.objects.get(id= int(id))
        customer = month.customer

        date = month.came_and_went.split(',')
        data_list =list()
        for i in date :
            if len(i) == 10 :
                data_list.append(i[5:])
        context ={
                'data_list':data_list,
                'month':month
                ,'customer':customer
                }
        return render (request,'customer/customer-month.html',context)
class DeleteCustomer(View):
    @user_chief
    def post(self,request,pk):
        customer =  Customer.objects.get(id=int(pk))
        customer.delete()
        return redirect('main:home_admin')

class DeleteCustomerEucator(View):
    @user_educator
    def post(self,request,pk):
        customer =  Customer.objects.get(id=int(pk))
        customer.delete()
        return redirect('main:home')
