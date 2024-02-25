from django.urls import path
from django.http import HttpRequest
from . import views

urlpatterns = [
    path('',views.dashboard),
    path('#',views.dashboard),
    path('dashboard',views.dashboard),
    path("dashboard/_Filter_timeline_toda",views.dashboard),
    path('sessions',views.sessions),
    path('payments/history',views.history),
    path('payments',views.history),
    path('payments/input',views.payment_input),
    path('payments/input/submit',views.payment_submit),
    path('accounts',views.account),
    path('accounts/account',views.account_edit),
    path('user/profile',views.account_edit),
    

]