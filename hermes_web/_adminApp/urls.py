from django.urls import path
from django.http import HttpRequest
from . import views

urlpatterns = [
    path('',views.login_verif,name='login'),
    path('login',views.login_verif,name='login'),
    path('logout',views.logout_view,name='logout'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('sessions',views.sessions,name='sessions'),
    path('payments/history',views.history,name='payment'),
    path('payments',views.history,name='payment'),
    path('payments/input',views.payment_input,name='paymentInput'),
    path('payments/input/submit',views.payment_submit,name='paymentSubmit'),
    path('accounts',views.account,name='account'),
    path('accounts/account',views.account_edit,name='accountEdit'),
    path('users/profile',views.account_edit,name='accountEdit'),
    path('users/add',views.add_user,name='accountAdd'),
    path('packages',views.packages,name='packages'),
]

