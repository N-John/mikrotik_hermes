import time
import datetime as dt
from datetime import datetime, date, timedelta
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
import json


from .models import Payment,Pkgs,Logs
from .models import Users,Sessions,Finances

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
    ldat.save(using='webdb')

def dashboard(request):

    all_payments = Payment.objects.all()

    filter_param = request.GET.get('filter', None)
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
                  'logs':Logs.objects.using('webdb').all(),
                  'persentage_pay_change':'100',
                  'persentage_pay_type':'increase',
                  'Timeline_filter':'All',
                  'total_revenue': totalRevenue,
                  'persentage_total_revenue_change': '100',
                  'persentage_total_revenue_type': 'increase',
                  'no_of_customers': len(Users.objects.all()),
                  'no_of_active_customers': len(Sessions.objects.filter(status="active")),
                    'sales': all_payments,
                    'payment_graph': json.dumps(payment_graph),
                    'revenue_graph': json.dumps(revenue_graph),
                    'customers_graph': json.dumps(customers_graph),
                    'time_graph': json.dumps(time_graph),
                      }
        return render(request,'admin_dashboard.html',dataform)
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
                  'logs':Logs.objects.using('webdb').all(),
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
                  'logs':Logs.objects.using('webdb').all(),
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
                      }
        return render(request,'admin_dashboard.html',dataform)


def payment_input(request):
    filter_param = request.GET.get('account', None)
    

    if not filter_param == None:
        account_data=Users.objects.get(acc=filter_param)

        dataform = {"account_no":account_data.acc}
        return render(request,'pages-payments.html',dataform)


    return render(request,'pages-payments.html')
    

def payment_submit(request):
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

    datafield={"transacc":account_no,
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
            datafield['session_creation']='created'
            
        
        #false
        else:
            print('Not enough balance to create new sessions')
            datafield['session_creation']='insufficient'
            log('error',f'Fail create new user session. Insufficient balance')
                #notify of insuficient funds
    
    #True
    else:
        print('user already has an active session')
        datafield['session_creation']='existed'
    
    return render(request,'payment_confim.html',datafield)

def sessions(request):
    all_sessions = Sessions.objects.all()
    active_sessions = Sessions.objects.filter(status="active")
    total_act=len(active_sessions)
    total_hist=len(all_sessions)
    dataform={'session_data':all_sessions,
              "active_session":active_sessions,
              'total_act':total_act,
              'total_hist':total_hist,
              }

    return render(request,'wired_active.html',dataform)

def history(request):
    all_payments = Payment.objects.all()
    filter_param = request.GET.get('filter', None)

    #total revenue
    totalRevenue=0
    for payment in all_payments:
        totalRevenue=totalRevenue+payment.amount
    dataform={'no_of_payments': len(all_payments),
              'total_revenue': totalRevenue,
              'no_of_customers': len(Users.objects.all()),
                'sales': all_payments,

                  }
    return render(request,'wired_history.html',dataform)

def account(request):
    filter_param = request.GET.get('account', None)

    all_users = Users.objects.all()
    dataField={'acc_data': all_users}
     
    return render(request,'wired_account.html',dataField)


def account_edit(request):
    account_select = request.GET.get('account', None)
    print(account_select)
    if account_select==None:
        return render(request,'wired_acc_edit.html')
    
    else:

        account_select_data=Users.objects.get(acc=account_select)
        finances_selected=Finances.objects.filter(acc=account_select)
        sessions_selected=Sessions.objects.filter(acc=account_select)
        pkg_options=Pkgs.objects.all()

        dataform={
            'acc':account_select,
            'name':account_select_data.name,
            'username':account_select_data.username,
            'password':account_select_data.password,
            'phone':account_select_data.phone,
            'package':Pkgs.objects.get(pno=account_select_data.package),
            'pkg_options':pkg_options,
            'balance':account_select_data.balance,
            'finances':finances_selected,
            'sessions':sessions_selected
        }
        return render(request,'wired_acc_edit.html',dataform)

def profile(request):
    return render(request,'user-profile.html')

