from django.shortcuts import render , redirect
from django.views import View
from .models import *
from django.contrib import messages
from .help import CheckUserData
from .decorator import  user_chief ,user_chief_fun


class Home_admin_View(CheckUserData,View):
    @user_chief
    def get(self,request):
        user = request.user.user
        token_id = user.token_id
        educator = Client.objects.filter(token_code=token_id).prefetch_related('educators','months_chiefs')
        month =  Month.objects.filter(chief=user).order_by('-id')
        context={
            'user':user,
            'educator':educator,
            'month':month
        }
        return render (request,'admin/admin.html',context)


class CreateCustomerAdminView(View):
    @user_chief
    def post(self,request):
        user = request.user.user
        educator = request.POST.get('educator')
        educator = Client.objects.get(id = int(educator))
        name = request.POST.get('name')
        name = name.replace("о","o")
        phone = request.POST.get('phone')
        phone =  phone.replace("о","o")
        total_summa = request.POST.get('total_summa')
        customer = Customer.objects.create(chief= user, educator=educator,name=name,phone=str(phone),total_summa=int(total_summa))
        if customer:
            Month.objects.create(customer=customer,total_summa = int(total_summa))
            messages.success(request, f"Бола К,у'шилди")
        return redirect('main:home_admin')



class EducatorsAdminView(View):
    @user_chief
    def get(self,request,pk):
        user = request.user.user
        educator = Client.objects.get(id=int(pk))
        customer = Customer.objects.filter(educator=educator).prefetch_related('months_customers')
        return render(request,'admin/educator-customer.html',{'customer':customer , 'e': educator} )

class  TransferAdminView(View):
    @user_chief
    def get(self,request):
        user = request.user.user
        transfer =  Transfer.objects.filter(chief= str(user.name) ).order_by('-id')
        return render(request,'admin/transfer.html',{'transfer':transfer})
    @user_chief
    def post(self,request):
        user = request.user.user
        educator = request.POST.get('educator')
        educator = Client.objects.get(name=educator)
        transfer = request.POST.get('transfer')
        summa = int(request.POST.get('summa'))
        if transfer == 'transfer':
            if  user.balans_summa >= int(summa):
                user.balans_summa-= int(summa)
                user.save()
                educator.balans_summa+= int(summa)
                educator.save()
                Transfer.objects.create(chief=user.name,educator=educator.name,summa=summa,text='>>' )
                messages.success(request, f" O'tkazma Amakga Oshdi ")
            else:
                messages.success(request, f" O'tkazma Bajarilmadi  ")
        elif transfer == 'un_transfer':
            if  educator.balans_summa >= summa:
                educator.balans_summa-= summa
                educator.save()
                user.balans_summa+= summa
                user.save()
                Transfer.objects.create(chief=user.name,educator=educator.name,summa= summa , text='<<' )
                messages.success(request, f" O'tkazma Amakga Oshdi ")
            else:
                messages.success(request, f" O'tkazma Bajarilmadi  ")
        return redirect('main:home_admin')



class CostAdminView(View):
    @user_chief
    def get(self,request):
        user = request.user.user
        cost = user.cost_chiefs.all().order_by('-id')
        return render(request , 'admin/cost.html',{'cost':cost})
    @user_chief
    def post(self,request):
        user = request.user.user
        summa = request.POST.get('pul')
        text = request.POST.get('text')
        text = text.replace("о","o")
        month = user.months_chiefs.all().order_by('-id')[0]
        Cost.objects.create( chief = user, month=month,summa=int(summa),text=text,name=user.name)
        user.balans_summa -= int(summa)
        user.save()
        messages.success(request, "Чк,им  Амалга ошди ")
        return redirect('main:home_admin')


@user_chief_fun
def update_working_day(request):
    if request.method == 'POST':
        working_day = request.POST['working_day']
        user = request.user.user
        user.working_day = working_day
        user.save()
    return redirect('main:home_admin')

class Payment_adminView(View):
    @user_chief
    def get(self,request):
        payment =  request.user.user.cpayment_chiefs.all().order_by('-id').select_related('customer')
        return render (request,'admin/pay-detail.html',{'payment':payment})

class CostVznosAdminView(View):
    @user_chief
    def get(self,request):
        user = request.user.user
        month = Month.objects.filter(chief=user).order_by('-id').prefetch_related('cost_months')
        return render (request,'admin/cost-vznos.html',{'month':month})