import time
import datetime as dt
from datetime import datetime, date, timedelta
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
import json
from django.views.decorators.csrf import csrf_exempt
#from django.shortcuts import render

# Create your views here.

from .models import apiData,api_sms
from _adminApp.models import Users,pppoe,Contacts,Logs,Payment,Finances


from _adminApp.hermes import hermes

def RED(txt:str):
    return '\033[91m'+str(txt)+'\033[0m'
def GREEN(txt:str):
    return '\033[92m'+str(txt)+'\033[0m'
def MENU(txt:str):
    return '\033[36m'+str(txt)+'\033[0m'

def tme():
    TME=time.ctime().split(' ')
    tme=f"[{TME[-3]}-{TME[1]}-{TME[-1]} {TME[-2]}] "
    return tme

def log(topic:str,dsc:str):
    TME=time.ctime().split(' ')
    L_DATE=f'{TME[-3]}-{TME[1]}-{TME[-1]}'
    L_TIME = datetime.strptime(TME[-2], "%H:%M:%S").strftime("%I:%M %p")
    ldat=Logs(topic=topic,date=L_DATE,time=L_TIME,desc=dsc)
    ldat.save(using='webdb')


@csrf_exempt
def bot_post(request):#bot posts its data to be assessed
    btoken=request.META['HTTP_AUTHENT']
    if not apiData.objects.filter(tokens=btoken).exists():
        print('INVALID API TOKEN')
        return HttpResponse(status=404)

    if not request.method == 'POST':
        return HttpResponse('POST FORM ERROR',status=400)
    
    bdy=request.body.decode('utf-8')
    try:
        payload = json.loads(bdy)
        print('Payload json decoded')
        print(f"Payload: {payload}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return HttpResponse(status=400)
    
    
    if payload['posting'] == 'MPESA':
        print('MPESA POSTING')
        FDATE=payload['date']
        FTIME=payload['time']
        FSOURCE=payload['source']
        FCONT=payload['smsContent']
        print(f'{"-"*50}\nDate: {FDATE}\nTime : {FTIME}\nSource : {FSOURCE}\nContent : {FCONT}\n{"-"*50}')

        date_object = datetime.strptime(FDATE, '%y/%m/%d')
        formatted_date = date_object.strftime('%d-%b-%Y')
        time_object = datetime.strptime(FTIME, '%H:%M:%S')
        formatted_time = time_object.strftime('%I:%M %p')
        
        sdat=api_sms(source =FSOURCE,date = formatted_date,time = formatted_time,message = FCONT,read = 'False')
        sdat.save()

        CONTACTS=Contacts.objects.all()
        sendr=''
        amnt=0
        for cont in CONTACTS:
            if cont.contact in FCONT:
                sendr=cont.contact
                amnt=int(FCONT.strip().split('received Ksh')[1].split('.')[0])
                break
            
        if not sendr =='':
            trans_code=FCONT.strip().split(' ')[0]
            print(f'SENDER FOUND \n     SENDER {sendr} :     \nAMOUNT: {amnt},     \nCode : {trans_code}')
            
            
            acc_no=Contacts.objects.get(contact=sendr).account

            pay_sub=Payment(acc=acc_no, code=trans_code, amount=amnt,source=sendr,date=formatted_date,time=formatted_time)
            pay_sub.save()

            fin_sub=Finances(acc=acc_no,moneyIn=amnt,moneyOut=0.00,description='Bot Payment',date=formatted_date)
            fin_sub.save()

            log('payment',f'Recieved BOT payment of ksh{amnt} with code {trans_code}')

            if Users.objects.filter(acc = acc_no).exists():
                acc_baled=Users.objects.get(acc=acc_no)
                acc_baled.balance=acc_baled.balance+amnt
                acc_baled.save()

            elif pppoe.objects.filter(acc=acc_no).exists():
                pacc_baled=pppoe.objects.get(acc=acc_no)
                pacc_baled.balance=pacc_baled.balance+amnt
                pacc_baled.save()
                
            else:
                print('ACCOUNT NOT FOUND IN AITHER PPPOE OR HOTSPOT')
                log(f'UNASIGNED PAYMENT FOR ACC {acc_no}. Account not found')
            

            cd,inf = hermes.userSessionMonitor(acc_no)
            print(f'Session monitor exit code [{cd}] with message [{inf}]')

        else:
            log(f'Got bot post DATE:{FDATE} TIME:{FTIME} SOURCE:{FSOURCE} CONTENT:{FCONT} BOTID: {btoken}','BOT TRANSMITION UNKNOWN')
            print('SENDER NOT FOUND')
            return HttpResponse('Sender not found')

        #print(f'BOT SUBMITTED A FORM \nDATE: {FDATE}\n    TIME: {FTIME}\n    SOURCE: {FSOURCE}\n      CONTENT: {FCONT}')
        return HttpResponse('OK')
    
    elif payload['posting'] == 'SMS':
        print('SMS POSTING')
        SMSTME=payload['time']
        DTE=payload['date']
        SENDER=payload['sender']
        MESS=payload['message']

        print(f'{"-"*50}\nDate: {DTE}\nTime : {SMSTME}\nSource : {SENDER}\nContent : {MESS}\n{"-"*50}')

        date_object = datetime.strptime(DTE, '%y/%m/%d')
        formatted_date = date_object.strftime('%d-%b-%Y')
        time_object = datetime.strptime(SMSTME, '%H:%M:%S')
        formatted_time = time_object.strftime('%I:%M %p')
        

        smsdat=api_sms(source =SENDER,date = formatted_date,time = formatted_time,message = MESS,read = 'False')
        smsdat.save()

        return HttpResponse(status=200)


    else:
        print('posting methord unavailable')
        return HttpResponse(status=418)



def bot_get(request):#bot request for form and csrf token
    token=str(request.META['HTTP_AUTHENT'])
    if apiData.objects.filter(tokens=token).exists():
        #return render(request,'botPayForm.html')
        return HttpResponse(status=200)
    else:
        print(f'INVALID API TOKEN :{str(token)}')
        return HttpResponse(status=404) 
 