from django.urls import path
from .views import  *
from .ajax import *
from .admin_views import * 
from .register_view import *
from .customer_view import *
app_name = 'main'


urlpatterns  = [
    path('', HomeView.as_view() , name='home'),
    path('chief', Home_admin_View.as_view() , name='home_admin'),

    path('signup',Register_chief_View.as_view(),name='signup'),
    path('signup/educator',Register_educator_View.as_view(),name='signup_educator'),

    path('login/',LoginView.as_view(),name='login'),
    path('accounts/logout/',logout_, name = 'logout'),

    path('update/working/day',update_working_day,name="update_working_day"),
    path('educators/admin/<int:pk>',EducatorsAdminView.as_view(), name = 'educators_admin'),

    path('create/customer/admin',CreateCustomerAdminView.as_view(),name='create_customer_admin'),
    path('create/customer',CreateCustomerView.as_view(),name='create_customer'),

    path('customer/came/and/went',came_and_went_admin, name='came_and_went_admin'),
    path('customer/came/and/went/educator',came_and_went_educator, name='came_and_went_educator'),

    path('customer/admin/<int:pk>',DetailCustomerView.as_view(),name='customer_admin'),
    path('customer/educator/<int:pk>',DetailCustomerEducatorView.as_view(),name='customer_educator'),


    path('customer/admin/update/<int:id>',Customer_updateView.as_view(), name='customer_admin_update'),
    path('customer/admin/update/educator/<int:id>',Customer_updateEducatorView.as_view(), name='customer_educator_update'),

    path('customer/month/detail/<int:id>',Customer_month_DetailView.as_view(), name='customer_month_detail'),
    path('customer/month/detail/educator/<int:id>',Customer_month_DetailViewEducator.as_view(), name='customer_month_detail_educator'),


    path('payment/admin',Payment_adminView.as_view(),name='payment_admin'),
    path('payment/educator',Payment_EducatorView.as_view(),name='payment_educator'),

    path('cost/admin',CostAdminView.as_view(),name='cost_admin'),
    path('cost/educator',CostEducatorView.as_view(),name='cost_educator'),

    path('cost/vznos/admin',CostVznosAdminView.as_view(),name='cost_vznos_admin'),
    path('delete/customer/<int:pk>',DeleteCustomer.as_view(),name='delete_customer'),
    path('delete/customer/educator/<int:pk>',DeleteCustomerEucator.as_view(),name='delete_customer_educator'),


    path('transfer/admin',TransferAdminView.as_view(),name='transfer'),
    path('transfer/educator',TransferEducatorView.as_view(),name='transfer_educator'),

#     path('cost',CostView.as_view(),name='cost'),
#     path('cost-payment',Cost_Payment_Summa.as_view(),name='cost_payment'),
]