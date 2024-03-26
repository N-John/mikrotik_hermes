from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpRequest,HttpResponseRedirect
from django.contrib.auth import authenticate, login,logout

from .userauth import userAuthenticate

from _adminApp.models import Payment,Pkgs,Logs,pppoe,Contacts
from _adminApp.models import Users,Sessions,Finances
from _adminApp.models import Notifications,Messages
#from .models import adminAccounts

import json
import time
import datetime as dt
from datetime import datetime, date, timedelta
import random


def MN(user:str):

    try:
        mess=Messages.objects.filter(to=user,read=False)
        notif=Notifications.objects.filter(to=user,read=False)
        msgs={}
        ntfs={}

        n=0
        for nf in notif:
            n+=1
            ntfs[n]={"type":nf.category,
                    "topic":nf.topic,
                    "message":nf.notification,
                    'nid':nf.id}
            

        m=0
        for ms in mess:
            m+=1
            msgs[m]={"name":ms.sender,
                    "message":ms.message,
                    'mid':ms.id}                

        return 1,  msgs, ntfs

    except Exception as e:
        return 0,msgs,ntfs

def calculate_percentage_change(old_value, new_value):
    if old_value == 0:
        if new_value == 0:
            percentage_change = 0
        else:
            percentage_change = float('inf') if new_value > 0 else float('-inf')
    else:
        percentage_change = ((new_value - old_value) / old_value) * 100
    if percentage_change > 0:
        change_type = "increase"
    elif percentage_change < 0:
        change_type = "decrease"
    else:
        change_type = "no change"
    percentage_change=str(percentage_change).replace('-','')
    return percentage_change, change_type

def log(topic:str,dsc:str):
    TME=time.ctime().split(' ')
    L_DATE=f'{TME[-3]}-{TME[1]}-{TME[-1]}'
    L_TIME = datetime.strptime(TME[-2], "%H:%M:%S").strftime("%I:%M %p")
    ldat=Logs(topic=topic,date=L_DATE,time=L_TIME,desc=dsc)
    ldat.save()

def tme():
    TME=time.ctime().split(' ')
    L_DATE=f'{TME[-3]}-{TME[1]}-{TME[-1]}'
    L_TIME = datetime.strptime(TME[-2], "%H:%M:%S").strftime("%I:%M %p")
    return f'{L_DATE} {L_TIME}'

def notif(topic:str,message:str,recipient:str,category:str):
    #NOTIFICATION category CAN EITHER BE WARNING,DANGER OR SUCCESS
    recipientAccounts=[]
    if recipient.lower() == "all":
        for usr in Users.objects.all():
            recipientAccounts.append(usr.username)
    else:
        if Users.objects.filter(acc=recipient).exists():
            recipientAccounts.append(Users.objects.get(acc=recipient))
            
    for recipientAccount in recipientAccounts:
        addNotification=Notifications(topic= topic,#heading of notificcation
                                        category    = category,#WARNING,DANGER OR SUCCESS
                                        to          = recipientAccount,#recipient
                                        dateTime    = tme(),  
                                        notification= message, 
                                        read        = False
                                        )
        addNotification.save()
    
    return 1
    
##############################

def publicLogin_view(request):
    print('Login requested')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #user = authenticate(request, username=username, password=password)
        user=userAuthenticate(request=request,username=username,password=password)
        if user is not None:
            login(request, user)
            print(user)
            log('User,Login',f'{user} Logged in')
            return redirect('dashboard')  # Redirect to a success page
        else:
            log('Login,Error',f'{username} Failed log in')
            return render(request, 'page-login.html', {'err': True,"err_mess":'Invalid username or password'})
    else:
        #return redirect('/admin/')
        return render(request, 'page-login.html')

def publicLogout_view(request):
    usr=request.user.username
    print(f'{usr} Logged Out')
    logout(request)
    log('User,Logout',f'User {usr} Logged Out')

    return redirect('/login')  # Redirect to the login page

def publicDashboard(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    
    all_payments = Payment.objects.all()
    filter_param = request.GET.get('filter', None)

    dataform={}
    status,dataform['messages'],dataform['notifications'] = MN(request.user.username)
    #ALL
    if filter_param == None:
        #total revenue
        totalRevenue=0

        payment_graph=[]
        revenue_graph=[]
        customers_graph=[]
        time_graph=[]

        for payment in all_payments:
            dates=dt.datetime.strptime(payment.date, "%d-%b-%Y").date()
            times=dt.datetime.strptime(payment.time, "%I:%M %p").time()

            totalRevenue=totalRevenue+payment.amount

            payment_graph.append(len(all_payments))
            revenue_graph.append(totalRevenue)
            customers_graph.append(len(Users.objects.all()))
            datetime_obj = dt.datetime.combine(dates, times)
            formatted_datetime = datetime_obj.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            time_graph.append(formatted_datetime)

        
           
        dataform={'no_of_payments': len(all_payments),
                  'logs':Logs.objects.all().order_by('-lid')[:10],
                  'persentage_pay_change':'100',
                  'persentage_pay_type':'increase',
                  'Timeline_filter':'All',
                  'total_revenue': totalRevenue,
                  'persentage_total_revenue_change': '100',
                  'persentage_total_revenue_type': 'increase',
                  'no_of_customers': len(Users.objects.all()),
                  'no_of_active_customers': len(Sessions.objects.filter(status="active")),
                    'sales': all_payments,
                    'hotspot_users_count':len(pppoe.objects.all())
                      }
        
        return render(request,'publicDashboard.html',dataform)
    #TODAY
    elif filter_param == 'Today':
        #total revenue
        totalRevenueToday=0
        totalRevenueYesterday=0
        no_of_paymentsToday=0
        no_of_paymentsYesterday=0
        today=date.today()
        day_before_today = today - timedelta(days=1)

        payment_graph=[]
        revenue_graph=[]
        customers_graph=[]
        time_graph=[]
        
        for payment in all_payments:
            dates=dt.datetime.strptime(payment.date, "%d-%b-%Y").date()
            times=dt.datetime.strptime(payment.time, "%I:%M %p").time()
            if dates==today:
                no_of_paymentsToday=no_of_paymentsToday+1
                totalRevenueToday=totalRevenueToday+payment.amount
                payment_graph.append(no_of_paymentsToday)
                revenue_graph.append(totalRevenueToday)
                customers_graph.append(len(Users.objects.all()))

                datetime_obj = dt.datetime.combine(dates, times)
                formatted_datetime = datetime_obj.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                time_graph.append(formatted_datetime)
            
            elif dates==day_before_today:
                no_of_paymentsYesterday=no_of_paymentsYesterday+1
                totalRevenueYesterday=totalRevenueYesterday+payment.amount

        pay_pers , pay_typ = calculate_percentage_change(no_of_paymentsYesterday, no_of_paymentsToday)
        rev_pers , rev_typ = calculate_percentage_change(totalRevenueYesterday, totalRevenueToday)

        dataform={'no_of_payments': no_of_paymentsToday,
                  'logs':Logs.objects.all(),
                  'persentage_pay_change':pay_pers,
                  'persentage_pay_type':pay_typ,
                  'Timeline_filter':'Today',
                  'total_revenue': totalRevenueToday,
                  'persentage_total_revenue_change': rev_pers,
                  'persentage_total_revenue_type': rev_typ,
                  'no_of_customers': len(Users.objects.all()),
                  'no_of_active_customers': len(Sessions.objects.filter(status="active")),
                    'sales': all_payments,
                    'payment_graph': json.dumps(payment_graph),
                    'revenue_graph': json.dumps(revenue_graph),
                    'customers_graph': json.dumps(customers_graph),
                    'time_graph': json.dumps(time_graph),
                    'hotspot_users_count':len(pppoe.objects.all())
                      }
        
        dataform['notifications']={1:{"type":"warning",
                                    "topic":'testing',
                                    "message":'this is a test notification'}
                                }
        
        dataform['messages']={1:{"name":"joseph",
                                "message":"test message"},
                              2:{"name":"joe",
                                "message":"second testing  message"}
                            }
        
        return render(request,'admin_dashboard.html',dataform)
    elif filter_param == 'ThisMonth':
        #total revenue
        totalRevenueThisMonth=0
        totalRevenueLastMonth=0
        no_of_paymentsThisMonth=0
        no_of_paymentsLastMonth=0
        today=date.today()
        ThisMonthDate = today - timedelta(days=30)
        LastMonthDate = today - timedelta(days=60)
        
        payment_graph=[]
        revenue_graph=[]
        customers_graph=[]
        time_graph=[]

        for payment in all_payments:
            dates=dt.datetime.strptime(payment.date, "%d-%b-%Y").date()
            times=dt.datetime.strptime(payment.time, "%I:%M %p").time()

            if dates>=ThisMonthDate:
                no_of_paymentsThisMonth=no_of_paymentsThisMonth+1
                totalRevenueThisMonth=totalRevenueThisMonth+payment.amount

                payment_graph.append(no_of_paymentsThisMonth)
                revenue_graph.append(totalRevenueThisMonth)
                customers_graph.append(len(Users.objects.all()))

                datetime_obj = dt.datetime.combine(dates, times)
                formatted_datetime = datetime_obj.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                time_graph.append(formatted_datetime)
            
            elif dates>=LastMonthDate and dates<=ThisMonthDate:
                no_of_paymentsLastMonth=no_of_paymentsLastMonth+1
                totalRevenueLastMonth=totalRevenueLastMonth+payment.amount

        pay_pers , pay_typ = calculate_percentage_change(no_of_paymentsLastMonth, no_of_paymentsThisMonth)
        rev_pers , rev_typ = calculate_percentage_change(totalRevenueLastMonth, totalRevenueThisMonth)

        dataform={'no_of_payments': no_of_paymentsThisMonth,
                  'logs':Logs.objects.all(),
                  'persentage_pay_change':pay_pers,
                  'persentage_pay_type':pay_typ,
                  'Timeline_filter':'This Month',
                  'total_revenue': totalRevenueThisMonth,
                  'persentage_total_revenue_change': rev_pers,
                  'persentage_total_revenue_type': rev_typ,
                  'no_of_customers': len(Users.objects.all()),
                  'no_of_active_customers': len(Sessions.objects.filter(status="active")),
                    'sales': all_payments,
                    'payment_graph': payment_graph,
                    'revenue_graph': revenue_graph,
                    'customers_graph': customers_graph,
                    'time_graph': time_graph,
                    'hotspot_users_count':len(pppoe.objects.all())
                      }
        
        dataform['notifications']={1:{"type":"warning",
                                    "topic":'testing',
                                    "message":'this is a test notification'}
                                }
        
        dataform['messages']={1:{"name":"joseph",
                                "message":"test message"},
                              2:{"name":"joe",
                                "message":"second testing  message"}
                            }
        
        return render(request,'admin_dashboard.html',dataform)

def payment_input(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    filter_param = request.GET.get('account', None)

    dataform={}
    status,dataform['messages'],dataform['notifications'] = MN(request.user.username)


    if not filter_param == None:
        account_data=Users.objects.get(acc=filter_param)

        dataform = {"account_no":account_data.acc}
        
        return render(request,'pages-payments.html',dataform)


    return render(request,'pages-payments.html')
    
def payment_submit(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    
    trans_code = request.POST['pay_code']
    account_no=request.POST['account_no']
    source=request.POST['pay_source']
    date=request.POST['pay_date']
    trans_time=request.POST['pay_time']
    rsel=request.POST['gridRadios']
    trans_amount=request.POST['pay_amount']
    

    date_object = datetime.strptime(date, '%Y-%m-%d')
    formatted_date = date_object.strftime('%d-%b-%Y')

    time_object = datetime.strptime(trans_time, '%H:%M')
    formatted_time = time_object.strftime('%I:%M %p')

    print(trans_code,account_no,source,formatted_date,formatted_time,rsel)
    pay_sub=Payment(acc=account_no, code=trans_code, amount=trans_amount,source=source,date=formatted_date,time=formatted_time)
    fin_sub=Finances(acc=account_no,moneyIn=trans_amount,moneyOut=0.00,description='Web Payment',date=formatted_date)
    pay_sub.save()
    log('payment',f'Recieved payment of ksh{trans_amount} with code {trans_code}')
    fin_sub.save()
    

    

    user_db_ac=Users.objects.get(acc=account_no)
    new_bal=int(user_db_ac.balance)+int(trans_amount)
    user_db_ac.balance=new_bal
    user_db_ac.save()
    log('finance',f'Deposited {trans_amount} to acc {account_no}. Balance {new_bal}')


    fdo=Finances.objects.order_by('-fid').first()

    #print(account_no)

    dataform={}
    status,dataform['messages'],dataform['notifications'] = MN(request.user.username)

    dataform={"transacc":account_no,
               "transname":Users.objects.get(acc=account_no).name,
               "transpkg":Users.objects.get(acc=account_no).package,
               "transusrname":Users.objects.get(acc=account_no).username,
               "transusrbal":Users.objects.get(acc=account_no).balance,
               'transcode':trans_code,
               'transamount':trans_amount,
               'transdate':formatted_date,
               'transtime':formatted_time,
               'transfid':fdo.fid,
               'facc':fdo.acc,
               'fmin':fdo.moneyIn,
               'fmout':fdo.moneyOut,
               'fdate':fdo.date}


    #print(trans_code,account_no,source,date,time,rsel)
    

    #check if user has an active session
    user_active_session= Sessions.objects.filter(acc=account_no, status='active')


    if len(user_active_session)==0:#User has no active session
        #check if user has enough balance for next sesson
            #true
        user_dat=Users.objects.get(acc=account_no)

        pkg_dat=Pkgs.objects.get(pno=user_dat.package)

        if user_dat.balance >= pkg_dat.price:
            #make finance transaction
            finance_move=Finances(acc=account_no,moneyIn=0.00,moneyOut=pkg_dat.price,description='Session renewal',date=formatted_date)

            user_dat.balance=int(user_dat.balance)-int(pkg_dat.price)
            user_dat.save()
            finance_move.save()
            log('finance',f'Withdrew {pkg_dat.price} from account {user_dat.acc}. New balance {user_dat.balance}')

            #create new session
            TME=time.ctime().split(' ')
            S_DATE=f'{TME[-3]}-{TME[1]}-{TME[-1]}'
            S_TIME = datetime.strptime(TME[-2], "%H:%M:%S").strftime("%I:%M %p")
            E_DATE = (datetime.strptime(S_DATE, "%d-%b-%Y") + timedelta(days=pkg_dat.days)).strftime("%d-%b-%Y")
            session_creation=Sessions(acc=account_no,profile=pkg_dat.name,startDate=S_DATE,startTime=S_TIME,endDate=E_DATE, endTime=S_TIME,status='active')
            session_creation.save()
            dataform['session_creation']='created'
            
        
        #false
        else:
            print('Not enough balance to create new sessions')
            dataform['session_creation']='insufficient'
            log('error',f'Fail create new user session. Insufficient balance')
                #notify of insuficient funds
    
    #True
    else:
        print('user already has an active session')
        dataform['session_creation']='existed'
    
    return render(request,'payment_confim.html',dataform)

def sessionCreation(acc:str):

        #check if user has an active session
    user_active_session= Sessions.objects.filter(acc=acc, status='active')


    if len(user_active_session)==0:#User has no active session
        #check if user has enough balance for next sesson
            #true
        user_dat=Users.objects.get(acc=acc)

        pkg_dat=Pkgs.objects.get(pno=user_dat.package)

        if user_dat.balance >= pkg_dat.price:
            TME=time.ctime().split(' ')
            S_DATE=f'{TME[-3]}-{TME[1]}-{TME[-1]}'
            #make finance transaction
            finance_move=Finances(acc=acc,moneyIn=0.00,moneyOut=pkg_dat.price,description='Session renewal',date=S_DATE)

            user_dat.balance=int(user_dat.balance)-int(pkg_dat.price)
            user_dat.save()
            finance_move.save()
            log('finance',f'Withdrew {pkg_dat.price} from account {user_dat.acc}. New balance {user_dat.balance}')

            #create new session
            
            S_TIME = datetime.strptime(TME[-2], "%H:%M:%S").strftime("%I:%M %p")
            E_DATE = (datetime.strptime(S_DATE, "%d-%b-%Y") + timedelta(days=pkg_dat.days)).strftime("%d-%b-%Y")
            session_creation=Sessions(acc=acc,profile=pkg_dat.name,startDate=S_DATE,startTime=S_TIME,endDate=E_DATE, endTime=S_TIME,status='active')
            session_creation.save()
            print('session created')
            return 1
            
        
        #false
        else:
            print('Not enough balance to create new sessions')
            log('error',f'Fail create new user session. Insufficient balance')
                #notify of insuficient funds
            return 0
    
    #True
    else:
        print('user already has an active session')
        return 0

def publicSessions(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    dataform={}
    status,dataform['messages'],dataform['notifications'] = MN(request.user.username)

    all_sessions = Sessions.objects.all()
    active_sessions = Sessions.objects.filter(status="active")
    total_act=len(active_sessions)
    total_hist=len(all_sessions)
    dataform={'session_data':all_sessions,
              "active_session":active_sessions,
              'total_act':total_act,
              'total_hist':total_hist,
              }

    return render(request,'hermes_active.html',dataform)

def history(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    all_payments = Payment.objects.all()
    filter_param = request.GET.get('filter', None)

    dataform={}
    status,dataform['messages'],dataform['notifications'] = MN(request.user.username)

    #total revenue
    totalRevenue=0
    for payment in all_payments:
        totalRevenue=totalRevenue+payment.amount
    dataform={'no_of_payments': len(all_payments),
              'total_revenue': totalRevenue,
              'no_of_customers': len(Users.objects.all()),
                'sales': all_payments,

                  }
    return render(request,'hermes_history.html',dataform)

def publicAccount(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    aclog=request.user.username
    print(aclog)

    dataform={}
    status,dataform['messages'],dataform['notifications'] = MN(aclog)

    if request.method == 'POST':
        print(request.POST)
        acc_nmb=request.POST['acc_nmb']

        acc_phne=request.POST['account_edit_phone']
        if not Contacts.objects.filter(contact=acc_phne).exists():#if phone number has been edited
            ad_phn=Contacts(account = acc_nmb, contact=acc_phne )
            ad_phn.save()


        acc_edit_obj=Users.objects.get(acc=acc_nmb)
        acc_edit_obj.name=request.POST['account_edit_name']
        acc_edit_obj.username=request.POST['account_edit_username']
        acc_edit_obj.password=request.POST['account_edit_password']
        acc_edit_obj.phone=acc_phne
        acc_edit_obj.save()

        log('admin,user',f'user {acc_nmb} data edited by {aclog}')
        #hermes.userEdit()
        print(f'user {acc_nmb} data edited by {aclog}')

        return HttpResponseRedirect('dashboard')


    account_select = request.user.acc
    
    account_type=Pkgs.objects.get(pno=request.user.package).pkg_type

    if account_type=='hotspot':
        account_select_data=Users.objects.get(acc=account_select)
        finances_selected=Finances.objects.filter(acc=account_select)
        sessions_selected=Sessions.objects.filter(acc=account_select)
        pkg_options=Pkgs.objects.filter(pkg_type='hotspot')
        dataform={
            'acc':account_select,
            'name':account_select_data.name,
            'username':account_select_data.username,
            'password':account_select_data.password,
            'package':Pkgs.objects.get(pno=account_select_data.package).name,
            'phone':account_select_data.phone,
            'pkg_options':pkg_options,
            'balance':account_select_data.balance,
            'finances':finances_selected,
            'sessions':sessions_selected
        }
        return render(request,'publicAccount.html',dataform)
        
    elif account_type=='pppoe':
        account_select_data=pppoe.objects.get(acc=account_select)
        finances_selected=Finances.objects.filter(acc=account_select)
        sessions_selected=Sessions.objects.filter(acc=account_select)
        pkg_options=Pkgs.objects.filter(pkg_type='pppoe')
        dataform={
            'acc':account_select,
            'name':account_select_data.name,
            'username':account_select_data.username,
            'password':account_select_data.password,
            'phone':account_select_data.phone,
            'package':Pkgs.objects.get(pno=account_select_data.package).name,
            'pkg_options':pkg_options,
            'balance':account_select_data.balance,
            'finances':finances_selected,
            'sessions':sessions_selected
        }
        return render(request,'publicAccount.html',dataform)
    
    return (request,'publicAccount.html')

def account(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    
    filter_param = request.GET.get('account', None)

    dataform={}
    status,dataform['messages'],dataform['notifications'] = MN(request.user.username)

    all_users = Users.objects.all()

    dataform={'acc_data': all_users}
    dataform['pppoe_user_count']=len(pppoe.objects.all())
    dataform['hotspot_users_count']=len(Users.objects.all())
    dataform['pppoe_acc_data']=pppoe.objects.all()
     
    return render(request,'hermes_account.html',dataform)

def account_edit(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    dataform={}
    status,dataform['messages'],dataform['notifications'] = MN(request.user.username)

    if request.method == 'POST':
        print(request.POST)
        acc_nmb=request.POST['acc_nmb']

        acc_phne=request.POST['account_edit_phone']
        if not Contacts.objects.filter(contact=acc_phne).exists():#if phone number has been edited
            ad_phn=Contacts(account = acc_nmb, contact=acc_phne )
            ad_phn.save()


        acc_edit_obj=Users.objects.get(acc=acc_nmb)
        acc_edit_obj.name=request.POST['account_edit_name']
        acc_edit_obj.username=request.POST['account_edit_username']
        acc_edit_obj.password=request.POST['account_edit_password']
        acc_edit_obj.phone=acc_phne
        acc_edit_obj.balance=request.POST['account_edit_balance']
        acc_edit_obj.save()

        log('admin,user',f'user {acc_nmb} data edited by admin')
        #hermes.userEdit()
        print(f'user {acc_nmb} data edited by admin')

        return HttpResponseRedirect('/dashboard')


    account_select = request.GET.get('account', None)
    account_type=request.GET.get('type', None)

    if account_select==None:
        f=[]
        for ls in Pkgs.objects.all():
            f.append(ls)
        

        dataform={
                'acc':"",
                'name':"",
                'username':"",
                'password':"",
                'phone':"",
                'package':"Choose ...",
                'pkg_options':f,
                'balance':"",
                'finances':"",
                'sessions':""
            }
        return render(request,'hermes_acc_edit.html',dataform)
    
    else:
        print('*********************************')
        if account_type=='hotspot':
            print('*********************************')
            account_select_data=Users.objects.get(acc=account_select)
            finances_selected=Finances.objects.filter(acc=account_select)
            sessions_selected=Sessions.objects.filter(acc=account_select)
            pkg_options=Pkgs.objects.filter(pkg_type='hotspot')

            dataform={
                'acc':account_select,
                'name':account_select_data.name,
                'username':account_select_data.username,
                'password':account_select_data.password,
                'package':Pkgs.objects.get(pno=account_select_data.package).name,
                'phone':account_select_data.phone,
                'pkg_options':pkg_options,
                'balance':account_select_data.balance,
                'finances':finances_selected,
                'sessions':sessions_selected
            }
            return render(request,'hermes_acc_edit.html',dataform)
        
        elif account_type=='pppoe':
            print('*********************************')
            account_select_data=pppoe.objects.get(acc=account_select)
            finances_selected=Finances.objects.filter(acc=account_select)
            sessions_selected=Sessions.objects.filter(acc=account_select)
            pkg_options=Pkgs.objects.filter(pkg_type='pppoe')

            dataform={
                'acc':account_select,
                'name':account_select_data.name,
                'username':account_select_data.username,
                'password':account_select_data.password,
                'phone':account_select_data.phone,
                'package':Pkgs.objects.get(pno=account_select_data.package).name,
                'pkg_options':pkg_options,
                'balance':account_select_data.balance,
                'finances':finances_selected,
                'sessions':sessions_selected
            }
            return render(request,'hermes_acc_edit.html',dataform)
    return (request,'hermes_acc_edit.html')

def profile(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    dataform={}
    status,dataform['messages'],dataform['notifications'] = MN(request.user.username)
    return render(request,'user-profile.html',dataform)

def pppoe_account(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    dataform={}
    status,dataform['messages'],dataform['notifications'] = MN(request.user.username)
    return render(request,'user-profile.html',dataform )

def add_user(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    
    dataform={}
    status,dataform['messages'],dataform['notifications'] = MN(request.user.username)

    if request.method == 'POST':
        upkgType    =request.POST.get('packageType')


        if upkgType == 'pppoe':
            #Automatically creating a rundom account no
            while 1:
                randomAcc=f'Hrp{random.randint(1000, 9999)}'
                if not pppoe.objects.filter(acc=randomAcc).exists():
                    break
            pk=Pkgs.objects.get(name=request.POST.get('packageSelected')).pno

            addUser=pppoe(acc=randomAcc, 
                            phone=request.POST.get('contact'),
                            location=request.POST.get('address'),
                            ip      =request.POST.get('ip', None),
                            username=request.POST.get('username'),
                            password=request.POST.get('password'),
                            install_date=tme(),
                            name    =request.POST.get('name'),
                            package =pk,
                            balance =0.00,
                        )
            addUser.save()
            addContact=Contacts(account = randomAcc,
                                contact=request.POST.get('contact'))
            addContact.save()
            log('User,Add',f'New PPPoE user {randomAcc} Added by {request.user.username}')
            #hermes.addUser('pppoe',request.POST['name'],request.POST['username'],request.POST['password'],pk)
            
            return redirect(f'/accounts/account?account={randomAcc}')

        elif upkgType == 'hotspot':
            #Automatically creating a rundom account no
            while 1:
                randomAcc=f'Hrh{random.randint(1000, 9999)}'
                if not Users.objects.filter(acc=randomAcc).exists():
                    break
            pk=Pkgs.objects.get(name=request.POST.get('packageSelected')).pno
            addUser=Users(acc=randomAcc, 
                            phone=request.POST.get('contact'),
                            username=request.POST.get('username'),
                            password=request.POST.get('password'),
                            install_date=tme(),
                            name    =request.POST.get('name'),
                            package =pk,
                            balance =0.00,
                        )
            addUser.save()
            log('User,Add',f'New Hotspot user {randomAcc} Added by {request.user.username}')
            #hermes.addUser('hotspot',request.POST['name'],request.POST['username'],request.POST['password'],pk)
            return redirect(f'/accounts/account?account={randomAcc}')
        
        else:
            print('Package type uidentified')

    else:
        
        pt= request.GET.get('ptype')
        f=[]

        for ls in Pkgs.objects.filter(pkg_type=pt):
            f.append(ls)
        dataform={'package':'Select a Package',
                'pkg_options':f,
                'ipPlaceholder':'10.0.0.***',
                'pkgtype':pt}
        
        return render(request,'user_register.html',dataform)

def packages(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    dataform = {}
    status,dataform['messages'],dataform['notifications'] = MN(request.user.username)
    dataform['edit']=False

    spef = request.GET.get('pid',None)

    if request.method == 'POST':
        criteria=request.POST.get('formType')
        if criteria == 'add':#Adding a package
            addPackage=Pkgs(name  = request.POST.get('Name'),     
                        speed     = request.POST.get('speed'),     
                        days      = request.POST.get('duration'),  
                        max_users = request.POST.get('maximumUsers'),     
                        price     = request.POST.get('price'),    
                        pkg_type  = request.POST.get('packageType'), 
                        )
            addPackage.save()
            log('Package,Edit',f'Npythew Package {request.POST.get("Name")} Added By {request.user.username}')
            #hermes.addPackage()

        elif criteria == 'edit':#editing a package
            editpkg=Pkgs.objects.get(pno=request.POST.get('packageId'))
            editpkg.name  = request.POST.get('eName')
            editpkg.speed     = request.POST.get('espeed')     
            editpkg.days      = request.POST.get('eduration') 
            editpkg.max_users = request.POST.get('emaximumUsers')     
            editpkg.price     = request.POST.get('eprice')  
            editpkg.save()
            log('Package,Edit',f'Package {request.POST.get("Name")} edited By {request.user.username}')
            #hermes.editPackage()

    elif spef is not None:
        
        pdat=Pkgs.objects.get(pno=spef)
        dataform['edit']=True
        dataform['packageObj']=pdat
        
    
    
    dataform['hotspotObject'] = Pkgs.objects.filter(pkg_type='hotspot') 
    dataform['pppoeObject'] = Pkgs.objects.filter(pkg_type='pppoe')
    
                
        
    return render(request,'page-packages.html',dataform)