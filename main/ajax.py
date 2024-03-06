from django.http import JsonResponse
from .models import Month , Customer
import datetime
from .decorator import user_chief_fun

@user_chief_fun
def came_and_went_admin(request):
    online_date = str(datetime.date.today())
    user_id =  request.GET.get('user_id')
    customer = Customer.objects.get(id=int(user_id))
    true =  request.GET.get('keldi')
    month = customer.months_customers.all().order_by('-id')[0]
    if true == 'true':
        month_list = month.came_and_went.split(',')
        if online_date in month_list:
            customer.checked = True
            customer.save()
        else:

            customer.checked = True
            customer.save()
            month.came_and_went = month.came_and_went  +  online_date + ","
            month.save()
    if true == 'false':
        customer.checked = False
        customer.save()
        month_list = month.came_and_went.split(',')
        month_str = ''
        if online_date in month_list:
            for i in month_list:

                if online_date == i:
                    pass
                elif i == '':
                    pass
                else:
                    month_str += i +','
            month.came_and_went = month_str + ","
            month.save()
            customer.checked = False
            customer.save()
    return JsonResponse({'status':'ok'})


def came_and_went_educator(request):
    online_date = str(datetime.date.today())
    user_id =  request.GET.get('user_id')
    customer = Customer.objects.get(id=int(user_id))
    true =  request.GET.get('keldi')
    month = customer.months_customers.all().order_by('-id')[0]
    if true == 'true':
        month_list = month.came_and_went.split(',')
        if online_date in month_list:
            customer.checked = True
            customer.save()
        else:
            customer.checked = True
            customer.save()
            month.came_and_went = month.came_and_went  +  online_date + ","
            month.save()
    if true == 'false':
        customer.checked = False
        customer.save()
        month_list = month.came_and_went.split(',')
        month_str = ''
        if online_date in month_list:
            for i in month_list:

                if online_date == i:
                    pass
                elif i == '':
                    pass
                else:
                    month_str += i +','
            month.came_and_went = month_str + ","
            month.save()
            customer.checked = False
            customer.save()
    return JsonResponse({'status':'ok'})