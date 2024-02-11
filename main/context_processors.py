import datetime
from main.models import *
def create_month(request):
    online_date = datetime.date.today()
    user = request.user
    if user.is_staff:
        return ({'status':'ok'})
    if user.is_authenticated:
        date  = str(user.date_joined)
        date = date[:7]
        month = str(online_date)[:7]
        if date != month:
            client = user.user
            if client.chief == True:
                educator = Client.objects.filter(token_code = client.token_id)
                customer =  Customer.objects.filter(chief=client)
                for i in customer:
                    Month.objects.create(customer=i,total_summa = i.total_summa)
                for i in educator:
                    i.user.date_joined = online_date
                    i.user.save()
                    Month.objects.create(educator=i)
                Month.objects.create(chief=client)
                client.user.date_joined = online_date
                client.user.save()
            elif Client.chief == False:
                chief = Client.objects.filter( token_id = client.token_code)
                educator = Client.objects.filter(token_code = chief.token_id)
                customer =  Customer.objects.filter(chief=chief)
                for i in customer:
                    i.user.date_joined = online_date
                    i.user.save()
                    Month.objects.create(customer=i,total_summa = i.total_summa)
                for i in educator:
                    Month.objects.create(educator=i)
                Month.objects.create(chief=chief)
                chief.user.date_joined = online_date
                chief.user.save()
    return {'status':online_date}


def came_and_went_true_false(request):
    online_date = datetime.date.today()
    """ chief malumotlarini beradi  """
    user = request.user
    if user.is_staff:
        return ({'status':'ok'})
    if user.is_authenticated:
        date  = str(user.user.data)
        date = date[:10]
        month = str(online_date)[:10]
        if date != month:
            client = user.user
            if client.chief == True:
                educator = Client.objects.filter(token_code = client.token_id)
                customer =  Customer.objects.filter(chief=client)
                client.data = online_date
                client.save()
                for i in educator:
                    i.data = online_date
                    i.save()
                for i in customer:
                    if i.checked == False:
                        continue
                    i.checked = False
                    i.save()
            elif Client.chief == False:
                chief = Client.objects.filter( token_id = client.token_code)
                educator = Client.objects.filter(token_code = chief.token_id)
                customer =  Customer.objects.filter(chief=chief)
                chief.data = online_date
                chief.save()
                for i in educator:
                    i.data = online_date
                    i.data.save()
                for i in customer:
                    if i.checked == False:
                        continue
                    i.checked == False
                    i.save()
    return {'status':'ok'}