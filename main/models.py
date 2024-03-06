from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='user')
    name = models.CharField(max_length=15)
    working_day = models.PositiveIntegerField(default=22  ) # ish kuni
    phone = models.CharField(max_length=13)
    payment = models.BooleanField(default=True)
    data = models.DateField(auto_now_add=True)
    chief = models.BooleanField(default=False)
    token_id = models.CharField(max_length=10,blank=True)
    token_code = models.CharField(max_length=10,  blank=True)
    payment_summa = models.CharField('oylik tolov' , max_length=15,blank=True)
    balans_summa = models.IntegerField('balans summa' ,default=0)
    def __str__(self):
        return self.name

class Customer(models.Model):
    chief = models.ForeignKey(Client, on_delete=models.CASCADE , related_name='chiefs')
    educator = models.ForeignKey(Client,related_name='educators',on_delete=models.CASCADE)
    name = models.CharField(max_length=155)
    phone = models.CharField(max_length=13,null=True,blank=True)
    active = models.BooleanField(default=True)
    day_summa = models.BooleanField(default=False) # kunlik hisob kitob
    checked = models.BooleanField(default=False)
    total_summa = models.PositiveIntegerField('tolash kerak bolgan summa',default=0)
    def __str__(self):
        return self.name


class Month(models.Model):
    chief = models.ForeignKey(Client, on_delete=models.CASCADE , related_name='months_chiefs' , null=True,blank=True)
    educator = models.ForeignKey(Client,on_delete=models.CASCADE ,related_name='months_educators' , null=True,blank=True)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE ,related_name='months_customers' , null=True,blank=True)
    month = models.DateField(auto_now_add=True)
    came_and_went = models.TextField(blank=True) # bolani keldi kettisi hisoblaydi
    summa = models.PositiveIntegerField('Bolani  bergan summa',default=0)
    cost_summa = models.PositiveIntegerField('chqim summasi',default=0)
    total_summa = models.PositiveIntegerField('chief va educator Toplangan summa bolani berishi kerak bolgan summa ',default=0)
    def __str__(self):
        return f"{self.month}"

class Payment(models.Model):
    chief_user = models.ForeignKey(Client,on_delete=models.CASCADE,related_name='cpayment_chiefs', null=True,blank=True)
    educator= models.ForeignKey(Client ,on_delete =models.CASCADE, related_name='payment_educators' , null=True,blank=True)
    customer = models.ForeignKey(Customer  ,on_delete =models.CASCADE, related_name='payment_customers')
    user = models.CharField('tolovni kim oldi ' , max_length = 55 )
    date = models.DateField(auto_now_add=True)
    summa = models.PositiveIntegerField('tolangan summa',default=0)
    def __str__(self):
        return f" {self.customer.name } {self.summa}"


class Cost(models.Model):
    chief = models.ForeignKey(Client, on_delete=models.CASCADE,related_name='cost_chiefs')
    educator= models.ForeignKey(Client ,on_delete =models.CASCADE, related_name='cost_educators',null=True,blank=True)
    month = models.ForeignKey(Month, on_delete=models.CASCADE,related_name='cost_months')
    name = models.CharField('kim chiqim qilgan ',max_length=55)
    summa = models.PositiveIntegerField()
    text = models.TextField()
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return f'{self.summa}'


class Transfer (models.Model):
    chief = models.CharField('chief nameni saqlaydi ',max_length=30)
    educator = models.CharField(' educator nameni saqlaydi ',max_length=30)
    text = models.TextField()
    date = models.DateField(auto_now_add=True)
    summa = models.PositiveIntegerField()
    def __str__(self):
        return f'{self.summa} {self.text}'
