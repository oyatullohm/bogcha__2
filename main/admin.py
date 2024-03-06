from django.contrib import admin

from .models import * 
admin.site.register([Client,Customer,Month,Payment,Cost,Transfer])
