

from django.shortcuts import render , redirect
from django.views import View
from .models import *
from django.contrib import messages
from .decorator import user_educator

class HomeView(View):
    @user_educator
    def get(self,request):
        user = request.user.user
        chief = Client.objects.get(token_id=user.token_code)
        customer = user.educators.all().prefetch_related('months_customers').order_by('name')
        context={
            'user':user,
            'chief':chief,
            'customer':customer
        }

        return render (request,'educator/index.html',context)

class CreateCustomerView(View):
    def post(self,request):
        user = request.user.user
        chief =  Client.objects.get(token_id = user.token_code)
        name = request.POST.get('name')
        name = name.replace("о","o")
        phone = request.POST.get('phone')
        phone =  phone.replace("о","o")
        total_summa = request.POST.get('total_summa')
        customer = Customer.objects.create(chief= chief, educator=user,name=name,phone=str(phone),total_summa=int(total_summa))
        if customer:
            Month.objects.create(customer=customer,total_summa = int(total_summa))
            messages.success(request, f"Бола К,у'шилди")
        return redirect('main:home')

class DetailCustomerEducatorView(View):
    @user_educator
    def get(self,request,pk):
        user = request.user.user
        educator = Client.objects.filter(token_code = user.token_code)
        customer = Customer.objects.get(id=int(pk))
        month = Month.objects.filter(customer=customer).order_by('-id')
        context = {'month':month,'customer':customer ,'educator':educator}
        return render(request,'educator/educator-customer.html',context)
    @user_educator
    def post(self,request,pk):
        summa = request.POST.get('summa')
        month = request.POST.get('month')
        user = request.user.user
        customer = Customer.objects.get(id =int(pk))
        educator = customer.educator
        month = Month.objects.get(id=int(month))
        month.summa+=int(summa)
        month.save()
        month_chief = Month.objects.filter(chief=customer.chief).order_by('-id')[0]
        month_chief.total_summa += int(summa)
        month_chief.save()
        user.balans_summa += int(summa)
        user.save()
        Payment.objects.create(user=user.user  , chief_user=customer.chief , educator=educator , customer = customer , summa = int(summa))
        messages.success(request, " Тулов  Амалга ошди ")
        return redirect(f'/customer/admin/{pk}')

class Customer_updateEducatorView(View):
    @user_educator
    def post(self,request,id):
        user = request.user.user
        educator = Client.objects.filter(token_code = user.token_code)
        name = request.POST.get('name')
        name = name.replace("о","o")
        phone = request.POST.get('phone')
        phone = phone.replace("о","o")
        vznos = request.POST.get('vznos')
        active = request.POST.get('active')
        day_summa = request.POST.get('day_summa')
        customer = Customer.objects.get(id=int(id))
        educator = request.POST.get('educator')
        educator = Client.objects.get(id=int(educator))
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
        return redirect(f'/customer/educator/{id}')



class Customer_month_DetailViewEducator(View):
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


class TransferEducatorView(View):
    @user_educator
    def get(self,request):
        user = request.user.user
        transfer =  Transfer.objects.filter(educator= str(user.name) ).order_by('-id')
        return render(request,'educator/transfer.html',{'transfer':transfer})
    @user_educator
    def post(self,request):
        user = request.user.user
        chief = Client.objects.get(token_id = user.token_code)
        transfer = request.POST.get('transfer')
        summa = int(request.POST.get('summa'))
        if transfer == 'transfer':
            if  user.balans_summa >= int(summa):
                user.balans_summa-= int(summa)
                user.save()
                chief.balans_summa+= int(summa)
                chief.save()
                Transfer.objects.create(chief=chief.name,educator=user.name,summa=summa,text='<<' )
                messages.success(request, f" O'tkazma Amakga Oshdi ")
            else:
                messages.success(request, f" O'tkazma Bajarilmadi  ")
        elif transfer == 'un_transfer':
            if  chief.balans_summa >= summa:
                chief.balans_summa-= summa
                chief.save()
                user.balans_summa+= summa
                user.save()
                Transfer.objects.create(chief=chief.name,educator=user.name,summa= summa , text='>>' )
                messages.success(request, f" O'tkazma Amakga Oshdi ")
            else:
                messages.success(request, f" O'tkazma Bajarilmadi  ")
        return redirect('main:home')

class Payment_EducatorView(View):
    @user_educator
    def get(self,request):
        payment =  request.user.user.payment_educators.all().order_by('-id').select_related('customer')
        return render (request,'educator/pay-detail.html',{'payment':payment})

class CostEducatorView(View):
    @user_educator
    def get(self,request):
        user = request.user.user
        cost = Cost.objects.filter(name=user.name).order_by('-id')
        return render(request , 'educator/cost.html',{'cost':cost})
    @user_educator
    def post(self,request):
        user = request.user.user
        chief = Client.objects.get(token_id = user.token_code)
        summa = request.POST.get('pul')
        text = request.POST.get('text')
        text = text.replace("о","o")
        month = chief.months_chiefs.all().order_by('-id')[0]
        Cost.objects.create( chief = chief, month=month,summa=int(summa),text=text,name=user.name)
        user.balans_summa -= int(summa)
        user.save()
        messages.success(request, "Чк,им  Амалга ошди ")
        return redirect('main:home')




def handler_404(request,exception):
   return render(request, "404.html")

def handler_500(request):
    return render(request, "500.html")