from django.urls import path
from . import views
from django.shortcuts import render,redirect

def redir(request):
    req=request.path
    print(req)
    if req == '/c/':
        return redirect('register')
    elif req == '/':
        return redirect('/c/')

urlpatterns = [
    path('register',views.add_user,name='register'),
    path('',redir),
    path('login',views.publicLogin_view,name='login'),
    path('logout',views.publicLogout_view,name='logout'),
    path('dashboard',views.publicDashboard,name='dashboard'),
    path('sessions',views.publicSessions,name='sessions'),
    path('payments',views.history,name='payment'),
    path('payments/input',views.payment_input,name='paymentInput'),
    path('payments/input/submit',views.payment_submit,name='paymentSubmit'),
    path('account',views.publicAccount,name='account'),
    path('accounts/account',views.account_edit,name='accountEdit'),
    path('users/profile',views.account_edit,name='accountEdit'),
    path('packages',views.packages,name='packages'),
]

