from django.urls import path
from django.http import HttpRequest
from . import views
from django.shortcuts import redirect

def redir(request):
    req=request.path
    print(req)
    if req == '/a/':
        return redirect('alogin')
    
urlpatterns = [
    path('',redir),
    path('login',views.login_verif,name='alogin'),
    path('logout',views.logout_view,name='alogout'),
    path('dashboard',views.dashboard,name='adashboard'),
    path('sessions',views.sessions,name='asessions'),
    path('payments',views.history,name='apayment'),
    path('payments/input',views.payment_input,name='apaymentInput'),
    path('payments/input/submit',views.payment_submit,name='apaymentSubmit'),
    path('accounts',views.account,name='aaccount'),
    path('accounts/account',views.account_edit,name='aaccountEdit'),
    path('users/profile',views.account_edit,name='aaccountEdit'),
    path('users/add',views.add_user,name='aaccountAdd'),
    path('packages',views.packages,name='apackages'),
    path('sessions/mod',views.sessionMod,name='asessionMod'),
    
]
 
