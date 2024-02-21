from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
#from . import hermes
import os
import sqlite3

from .models import Payment,Active_sessions
#from models import 
#dtb=hermes.hermes()

def response(request):
    return render(request,"main.html",{'name':'john'})

def main(request):
    return render(request,"main.html")

def payment_input(request):
    return render(request,"payments_add.html")

def create_user(request):
    return render(request,"add_user.html")

def payment_history(request):
    all_payments = Payment.objects.all()

    # Iterate over the queryset and access the fields
    #for payment in all_payments:
        #print(payment.pid, payment.acc, payment.code, payment.amount, payment.source, payment.date, payment.time)
    return render(request,"payment_history.html", {"all_payments": all_payments})

def session_edit(request):
    return render(request,"edit_sessions.html")

def active_session(request):
    active_session=Active_sessions.objects.filter(status="active")

    return render(request,"active_sessions.html",{'active_session':active_session})

def payment_input_FORM(request):
    amount=request.POST['amount']
    contact=request.POST['source']
    code=request.POST['transaction_code']
    date=request.POST['date']
    time=request.POST['time']
    #print(d)

    return HttpResponse(f'AMOUNT: {amount}\nCONTACT: {contact}\nCODE: {code}\nDATE: {date}\nTIME: {time}')