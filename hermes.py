#MIT License
#
#Copyright (c) 2024 N-John
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.
##############################################################################################
import sqlite3 
from datetime import datetime , timedelta
import time
import paramiko
import os
import sys
#import threading
#import msvcrt

#VARIABLES
input_fl='variables.txt'
running = True
account_nme={}

#CACHE
cache_account={}
cache_contacts={}
cache_finances={}
cache_package={}
cache_payments={}
cache_sessions={}

lg='''
 _                                                         
| |__   ___ _ __ _ __ ___   ___  ___   ___  ___ _ ____   _(_) ___ ___
| '_ \ / _ \ '__| '_ ` _ \ / _ \/ __| / __|/ _ \ '__\ \ / / |/ __/ _ \\
| | | |  __/ |  | | | | | |  __/\__ \_\__ \  __/ |   \ V /| | (_|  __/
|_| |_|\___|_|  |_| |_| |_|\___||___(_)___/\___|_|    \_/ |_|\___\___|

HERMES SERVICE IS CREATED BY JOHN TO MANAGE MIKROTIK ISP SERVICES VIA HOTSPOT AND PPPoE.
To run this code, make sure you can connect to the router/server and to the sql server.
Make sure the "variables.txt" file has the appropriate data 

DISCLAIMER:
BEFORE RUNNING, MAKE SURE YOU HAVE THE FOLLOWING
    sqlite3     -> used for sql database
    paramiko    -> used for ssh communication
    time        -> 
    datetime    ->

OWNER: JOHN NJOROGE
GITHUB: https://github.com/N-John/mikrotik_hermes.git \n\n
LAST MODIFIED: 27-Jan-2024
    '''


def RED(txt:str):
    return '\033[91m'+str(txt)+'\033[0m'
def GREEN(txt:str):
    return '\033[92m'+str(txt)+'\033[0m'
def MENU(txt:str):
    return '\033[36m'+str(txt)+'\033[0m'

def tme():
    tme=f"[{time.ctime().strip().split(' ')[0]}, {time.ctime().strip().split(' ')[1]}/{time.ctime().strip().split(' ')[2]}/{time.ctime().strip().split(' ')[-1]} {time.ctime().strip().split(' ')[-2]}] "
    return tme


def log(dat:str):
    with open (log_file,'a') as log:
        log.write(f'\n {tme()} {dat}')
    #print(f'{tme()} {dat}')

def clear_terminal():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    else:
        # For Unix/Linux/MacOS
        print('\033c', end='')


def cache():
    try:
        print(tme()+'\033[92mUPDATING CACHE...[',end='')
        global cache_account
        global cache_contacts
        global cache_finances
        global cache_package
        global cache_payments
        global cache_sessions

        cache_account={}
        cache_contacts={}
        cache_finances={}
        cache_package={}
        cache_payments={}
        cache_sessions={}

        print('#'*10,end='')

        cx = sqlite3.connect(database)
        cu = cx.cursor()

        #account cache
        cu.execute("SELECT * FROM account")
        OUTPT=cu.fetchall()
        for data in OUTPT:
            cache_account[data[0]]={"name":data[1],
                                "phone"         :data[2],
                                "package"       :data[3],
                                "username"      :data[4],
                                "password"      :data[5],
                                "install date"  :data[6],
                                "balance"       :data[7],}
        
        print('#'*10,end='')

        #contacts cache
        cu.execute("SELECT * FROM contacts")
        OUTPT=cu.fetchall()
        for data in OUTPT:
            cache_contacts[data[2]]={"account":data[1],
                                "cid" :data[0],
                                }
        print('#'*10,end='')

        #finances  cache
        cu.execute("SELECT * FROM finances")
        OUTPT=cu.fetchall()
        for data in OUTPT:
            cache_finances[data[0]]={"account"  :data[1],
                                "money in"      :data[2],
                                "money out"     :data[3],
                                "date"          :data[4],
                                "description"   :data[5],
                                }
        print('#'*10,end='')

        #package cache
        cu.execute("SELECT * FROM package")
        OUTPT=cu.fetchall()
        for data in OUTPT:
            cache_package[data[0]]={"name"  :data[1],
                                "speed"     :data[2],
                                "days"      :data[3],
                                "max users" :data[4],
                                "price"     :data[5],
                                "type"      :data[6]
                                }
        print('#'*10,end='')

        #PAYMENT cache
        cu.execute("SELECT * FROM payments")
        OUTPT=cu.fetchall()
        for data in OUTPT:
            cache_payments[data[0]]={"account"  :data[1],
                                "code"          :data[2],
                                "amount"        :data[3],
                                "source"        :data[4],
                                "date"          :data[5],
                                "time"          :data[6]
                                }
        print('#'*10,end='')

        #sessions cache
        cu.execute('SELECT * FROM sessions where status = "active"')
        OUTPT=cu.fetchall()
        for data in OUTPT:
            cache_sessions[data[1]]={"sid"      :data[0],
                                "profile"       :data[2],
                                "start date"    :data[3],
                                "start time"    :data[4],
                                "end date"      :data[5],
                                "end time"      :data[6],
                                "status"        :data[7],
                                "creation date" :data[8]
                                }
        print(f"{'#'*10}] 100%\033[0m")
        cx.close()

        return 1
    except Exception as e:
        print(RED('#'*10))
        print(f'USER CASH FAIL: {str(e)}')
        return 0


def menu(menus:list):#A MODIFICATION OF https://github.com/N-John/mmenu.git
    try:
        #clear_terminal()
        #mnu=['\033[7m'+menus[n]+'\033[0m' if idx == n else item for idx, item in enumerate(menus)]
        while 1:
            print('     '+'+'+'-'*32+'+',flush=True)
            #print('\033[7m',end='')
            #print('     |'+' '*10+'\033[4mMENU\033[0m'+' '*18+'|',flush=True)
            c=0
            for mn in menus:
                gp=27-len(menus[c])
                c=c+1
                print(f'     | ({c}) {mn}'+' '*gp+'|',flush=True)
            print('     '+'+'+'-'*32+'+',flush=True)
            outpt=input('\n\n INPUT :==> ')
            if int(outpt) > 0 and int(outpt) <= len(menus):
                break
            else:
                cnf = input('INVALID INPUT. Do you want to exit [Y/N]? ')
                if cnf.strip().capitalize() == 'Y':
                    return -1
        return int(outpt)
    except Exception as e:
        print(str(e))   
        log(f'ERROR RUNNING MENU: {str(e)}')     
        return -1        


class hermes:
    def ssh_command(cmd):
        # Establish SSH connection to the MikroTik router
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=mk_ip, username=mk_username, password=mk_password)
            print(GREEN(f"{tme()}CONNECTED TO SERVER VIA SSH"))
            print(f'Running command [{cmd}]')
            stdin, stdout, stderr = ssh_client.exec_command(cmd)
            output = stdout.read().decode('utf-8')
            print(MENU(output))
            ssh_client.close()
            return str(output)

        except paramiko.AuthenticationException:
            print(RED(f"{tme()}Authentication failed, please check your credentials."))
            log('ERROR CONNECTING TO SSH SERVER: AUTHENTICATION FAIL')
            return f"Authentication failed, please check your credentials: {ssh_err}"
        
        except paramiko.SSHException as ssh_err:
            print(RED(f"{tme()}Unable to establish SSH connection: {ssh_err}"))
            log(f"ERROR: Unable to establish SSH connection: {ssh_err}")
            return f"Unable to establish SSH connection: {ssh_err}"
        
        except Exception as e:
            print(RED(f"{tme()}An error occurred: {e}"))

            log(f"SSH ERROR OCCURED: {e}")
            return f"An error occurred: {e}"
        
    def dbcommunication(comm:str):
        try:
            print(f'Running db communication command [{comm}]')
            cx = sqlite3.connect(database)
            cu = cx.cursor()
            cu.execute(comm)
            OUTPT=cu.fetchall()
            cx.commit()
            cx.close()
            print(OUTPT)
            return OUTPT

        except Exception as e:
            print(RED(f'FAILED SQL: {str(e)}'))
            return 0
    
    def payments(code:str,amount:str,source:str,date:str,time_tm:str):
        try:
            print(tme()+'RUNNING PAYMENT CHECKER')
            acc=''

            contacts=list(cache_contacts.keys())
            if not source in contacts:
                print(RED(f'SOURCE {source} PROVIDED DOES NOT EXIST.'))
                cnf=input('Do you want to add contact [Y/N]? ')
                if cnf.strip().capitalize()=='Y':
                    print("SELECT USER ACCOUNT: ")
                    ld_list=[]
                    for ch in cache_account:
                        ld_list.append(f"{cache_account[ch]['name']} : {ch}")

                    otp=menu(ld_list)-1
                    cnf = input(f'CONFIRM {ld_list[otp]} [Y/N] ')
                    if cnf.strip().capitalize() == 'Y':
                        
                        print(GREEN('CONFIRMED..'))
                        acc=ld_list[otp].split(':')[1].strip()
                        phone=cache_account[ld_list[otp].split(':')[1].strip()]["phone"]
                        cx = sqlite3.connect(database)
                        cu = cx.cursor()
                        cu.execute(f'SELECT cid FROM contacts')
                        cid=str(int(cu.fetchall()[-1][0])+1)
                        cu.execute(f'INSERT INTO contacts VALUES({cid},"{acc}","{source}")')
                        cx.commit()
                        cx.close()
                        print(f'contact added: [{cid},"{acc}","{source}"]')
                        #hermes.dbcommunication(f'INSERT INTO contacts VALUES({cid},"{acc}","{phone}")')
                    else:
                        print('EXITING....')
                        return 0
                else:
                    print('EXITING...')
                    return 0

            else:
                acc = cache_contacts[source]['account']


            print(GREEN('Account determined as '+acc))

            cx = sqlite3.connect(database)
            cu = cx.cursor()
            cu.execute(f'SELECT pid FROM payments')
            pid=str(int(cu.fetchall()[-1][0])+1)
            
            cu.execute(f'insert into payments values ({pid},"{acc}","{code}",{amount},"{source}","{date}","{time_tm}")') 
            log(f'insert into payments values ({pid},"{acc}","{code}",{amount},"{source}","{date}","{time_tm}")')
            print('payment values added')
            #add to finances 
            print('adding to finance')
            cu.execute(f'SELECT fid FROM finances')
            fid=str(int(cu.fetchall()[-1][0])+1)
            cu.execute(f'insert into finances values ({fid},"{acc}",{amount},0.00,"DEPOSIT","{str(tme())}")')
            log(f'insert into finances values ({fid},"{acc}",{amount},0.00,"DEPOSIT","{str(tme())}")')

            #ADD MONEY TO USER ACCOUNT
            print('Adding money to user account')
            balance=cache_account[acc]['balance'] + int(amount)
            cu.execute(f'UPDATE account set balance = {str(balance)} WHERE acc = "{acc}";')
            log(f'UPDATE account set balance = {str(balance)} WHERE acc = "{acc}";')
            print(GREEN(f'{tme()} USER PAYMENT ADDED WITH VALUES: ({pid},\nname: "{account_nme[acc]}",\ncode : "{code}",\nammount : {amount},\nsource : "{source}",\ndate : "{date}",\ntime : "{time_tm}")'))
            cx.commit()
            cx.close()
            cache()

            hermes.session_monitor(acc)
            return 1
        except Exception as e:
            print(RED(f'FAILED ADD PAY: {str(e)}'))
            log(f'FAILED ADD PAY: {str(e)}')
            cx.close()
            return 0
    
    def session_monitor(sm_acc=None):
        try:
            #check if user has an active session. if so,leave.
            #else, get money from sm_acc and create a new session
            print("RUNNING SESSION MONITOR")
            cx = sqlite3.connect(database)
            cu = cx.cursor()

            if not sm_acc == None:#if a user is specified, check even they have an inactive session
                #print(f'SPECIAL session monitor for {account_nme[sm_acc]}')
                cu.execute(f'SELECT * FROM sessions WHERE acc = "{sm_acc}" AND status = "active"')
                acc_sess=cu.fetchall()

                if len(acc_sess) == 0: #if no active session create new session
                    print(f'User {account_nme[sm_acc]} has no active session.\n Creating session...')
                   
                    PKGU=cache_account[sm_acc]["package"]
                    BALU=cache_account[sm_acc]["balance"]
                    PKG_PRICEU=cache_package[PKGU]["price"]#PRICE OF THE PACKAGE
                    PKG_NAMEU=cache_package[PKGU]["name"]#NAME OF THE PACKAGE
                    days_to_addU=cache_package[PKGU]["days"]#HOW MANY DAYS THE PACKAGE COVERS
                    #print(f"PACKAGE = {PKG_NAMEU}")
                    #print(f"balance = {sdt[1]}")

                    if BALU >= PKG_PRICEU:#if balance is enough to parchase nxt package
                        #remove money from account
                        
                        cu.execute('SELECT * FROM finances ORDER BY fid desc limit 1')
                        fid=str(int(cu.fetchone()[0]) + 1)
                        cu.execute(f'insert into finances values ({str(len(cache_finances))},"{str(sm_acc)}",0.00,{str(cache_package[PKGU]["price"])},"{cache_package[PKGU]["name"]} SEBSCRIPTION RENEWAL","{str(tme())}")')
                        log(f'insert into finances values ({str(len(cache_finances))},"{str(sm_acc)}",0.00,{str(cache_package[PKGU]["price"])},"{cache_package[PKGU]["name"]} SEBSCRIPTION RENEWAL","{str(tme())}")')
                        BALU=BALU-PKG_PRICEU
                        cu.execute(f'UPDATE account set balance = {str(BALU)} WHERE acc = "{sm_acc}"')
                        log(f'UPDATE account set balance = {str(BALU)} WHERE acc = "{sm_acc}"')
                        print(f'{sm_acc} Balance updated to {BALU}')

                        #create next session
                        TME=time.ctime().split(' ')
                        S_DATE=f'{TME[-3]}-{TME[1]}-{TME[-1]}'
                        S_TIME = datetime.strptime(TME[-2], "%H:%M:%S").strftime("%I:%M %p")
                        E_DATE = (datetime.strptime(S_DATE, "%d-%b-%Y") + timedelta(days=days_to_addU)).strftime("%d-%b-%Y")
                        cu.execute('SELECT * FROM sessions ORDER BY sid desc limit 1')
                        log('SELECT * FROM sessions ORDER BY sid desc limit 1')
                        sid=str(int(cu.fetchone()[0]) + 1)
                        cu.execute(f'INSERT INTO sessions VALUES({sid},"{sm_acc}","{PKG_NAMEU}","{S_DATE}","{S_TIME}","{E_DATE}","{S_TIME}","active","{str(tme())}")')
                        log(f'INSERT INTO sessions VALUES({sid},"{sm_acc}","{PKG_NAMEU}","{S_DATE}","{S_TIME}","{E_DATE}","{S_TIME}","active","{str(tme())}")')  
                        print(GREEN(f'{tme()}New session is created for {account_nme[sm_acc]} with the following values. ({sid},package : "{PKG_NAMEU}",start date : "{S_DATE}",start time : "{S_TIME}",end date : "{E_DATE}", end time : "{S_TIME}","active")'))

                        if cache_package[cache_account[sm_acc]["package"]]["type"] == 'pppoe':
                            hermes.ssh_command(f'ppp secret set "{account_nme[sm_acc]}" disabled=no')
                        elif cache_package[cache_account[sm_acc]["package"]]["type"] == 'hotspot':
                            hermes.ssh_command(f'ip hotspot user set "{account_nme[sm_acc]}" limit-uptime=0')      

                    else:
                        print(f'USER {account_nme[sm_acc]} ACCOUNT BALANCE IS STILL INSUFFICIENT. NO SESSION CREATED') 

                else:
                    print(f'USER {account_nme[sm_acc]} ALREADY HAS AN ACTIVE SESSION.')           


            cu.execute('SELECT * FROM sessions WHERE status = "active"')           
            active_sess=cu.fetchall()

            for dat in active_sess:#loop through active sessions
                #print(f"{tme()} CHECKING ACTIVE SESSION {str(dat)}")

                #check if session is over
                combined_datetime = datetime.combine(datetime.strptime(dat[5], "%d-%b-%Y").date(), datetime.strptime(dat[6], "%I:%M %p").time())
                if combined_datetime <= datetime.now():
                    #(1) SET THE SESSION TO EXIRED
                    acc_no=dat[1]
                    print(f"SESSION EXPIRED FOR {account_nme[acc_no]}[{acc_no}]")
                    cu.execute(f'UPDATE sessions SET status = "expired" WHERE acc = "{acc_no}"')
                    log(f'UPDATE sessions SET status = "expired" WHERE acc = "{acc_no}"')

                    #(2)CHECK IF THE ACCOUNT HAS ENOUGH TO ACTIVATE THE NEXT SESSION
                    cu.execute(f'SELECT package,balance FROM account where  acc = "{acc_no}"')
                    sdt=cu.fetchall()[0]
                    PKG=sdt[0]
                    BAL=sdt[1]
                    cu.execute(f'SELECT price,name,days FROM package WHERE pno = {PKG}')
                    OTP=cu.fetchall()[0]
                    PKG_PRICE=OTP[0]
                    PKG_NAME=OTP[1]
                    days_to_add=OTP[2]

                    if BAL >= PKG_PRICE:#if balance is enough to parchase nxt package
                        #remove money from account
                        
                        cu.execute('SELECT * FROM finances ORDER BY fid desc limit 1')
                        fid=str(int(cu.fetchone()[0]) + 1)
                        cu.execute(f'insert into finances values ({str(fid)},"{str(acc_no)}",0.00,{str(PKG_PRICE)},"SEBSCRIPTION RENEWAL","{str(tme())}")')
                        log(f'insert into finances values ({str(fid)},"{str(acc_no)}",0.00,{str(PKG_PRICE)},"SEBSCRIPTION RENEWAL","{str(tme())}")')
                        BAL=BAL-PKG_PRICE
                        cu.execute(f'UPDATE account set balance = {str(BAL)} WHERE acc = "{acc_no}"')
                        log(f'UPDATE account set balance = {str(BAL)} WHERE acc = "{acc_no}"')
                        
                        #create next session                        
                        TME=time.ctime().split(' ')
                        S_DATE=f'{TME[-3]}-{TME[1]}-{TME[-1]}'
                        S_TIME = datetime.strptime(TME[-2], "%H:%M:%S").strftime("%I:%M %p")
                        E_DATE = (datetime.strptime(S_DATE, "%d-%b-%Y") + timedelta(days=days_to_add)).strftime("%d-%b-%Y")
                        cu.execute('SELECT * FROM sessions ORDER BY sid desc limit 1')
                        log('SELECT * FROM sessions ORDER BY sid desc limit 1')
                        sid=str(int(cu.fetchone()[0]) + 1)
                        cu.execute(f'INSERT INTO sessions VALUES({sid},"{acc_no}","{PKG_NAME}","{S_DATE}","{S_TIME}","{E_DATE}","{S_TIME}","active","{str(tme())}")')
                        log(f'INSERT INTO sessions VALUES({sid},"{acc_no}","{PKG_NAME}","{S_DATE}","{S_TIME}","{E_DATE}","{S_TIME}","active","{str(tme())}")')
                        print(GREEN(f'{tme()} NEW SESSION CREATED FOR {account_nme[acc_no]} WITH VALUES ({sid},package : "{PKG_NAME}",start date : "{S_DATE}",start time : "{S_TIME}",end date : "{E_DATE}",end time : "{S_TIME}","active","{str(tme())}")'))

                        #enable user on server
                        cu.execute(f'SELECT username FROM account where acc = "{acc_no}"')
                        un=cu.fetchall()[0][0]

                        if cache_package[cache_account[sm_acc]["package"]]["type"] == 'pppoe':
                            hermes.ssh_command(f'ppp secret set "{account_nme[sm_acc]}" disabled=no')
                        elif cache_package[cache_account[sm_acc]["package"]]["type"] == 'hotspot':
                            hermes.ssh_command(f'ip hotspot user set "{account_nme[sm_acc]}" limit-uptime=0')

                        #hermes.ssh_command(f'ip hotspot user set "{un}" limit-uptime=0')
                    

                    else:
                        #disable user session
                        print(f'{tme()} USER {account_nme[acc_no]} DISCONTINUED FROM CONNECTION')

                        if cache_package[cache_account[sm_acc]["package"]]["type"] == 'pppoe':
                            hermes.ssh_command(f'ppp secret set "{account_nme[sm_acc]}" disabled=yes')
                            hermes.ssh_command(f'ppp active remove [find name="{account_nme[sm_acc]}"]')
                        elif cache_package[cache_account[sm_acc]["package"]]["type"] == 'hotspot':
                            hermes.ssh_command(f'ip hotspot user set "{account_nme[acc_no]}" limit-uptime=1s')
                            hermes.ssh_command(f'ip hotspot active remove [find name="{account_nme[acc_no]}"]')

            cx.commit()
            cx.close()
            print('SESSION MONITOR COMPLETED')
            


        except Exception as e:
            cx.close()
            print(RED(f'FAILED SESSION MONITOR: {str(e)}'))
            log(f'FAILED SESSION MONITOR: {str(e)}')
            return 0

    def add_pkg(name:str,speed:int,days:int,users:str,price:int,p_type):
        try:
            
            cx = sqlite3.connect(database)
            cu = cx.cursor()
            pno=len(cache_package.keys())+1
            cu.execute(f'INSERT INTO package VALUES({pno},"{name}",{speed},{days},{users},{price},"{p_type}")')

        except Exception as e:
            print(RED(f'Package add error: [{str(e)}]'))   

    def add_user():
        try:
            print(MENU('ADDING USER: '))
            cx = sqlite3.connect(database)
            cu = cx.cursor()
            cu.execute('SELECT acc FROM account')
            aid=len(cu.fetchall()) + 5505
            cu.execute('SELECT pno,name FROM package')
            pkgs=cu.fetchall()
            cx.close()

            mikrotik_profs=['trial_profile','5mbps_hup','7mbps_hup','10MBPS_HUP']
            acc=f'WnWp{aid}'
            def_pkg=pkgs[1][1]
            def_pkg_no=pkgs[1][0]
            def_date_lst=time.ctime().strip().split(' ')
            def_date=f'{def_date_lst[2]}-{def_date_lst[1]}-{def_date_lst[4]}'
            
            while 1:
                name=input(MENU("Input the user's name: "))
                phne=input(MENU("Input their phone number: "))
                usernm=input(MENU("Input username: "))
                pswrd=input(MENU("Input password: "))
                

                inst_date=input(MENU(f"Input installation date: [{def_date}]"))
                if inst_date == '':
                    inst_date=def_date
                
                print(f'Available packages: \n{pkgs}')
                pkg = input(MENU(f'Select package: [{def_pkg}] => '))
                if pkg =='':
                    pkg = str(def_pkg_no)
                
                print(MENU(f"ACCOUNT : {acc}"))
                print(MENU(f"NAME : {name}"))
                print(MENU(f"PHONE : {phne}"))
                print(MENU(f"USERNAME : {usernm}"))
                print(MENU(f"PASSWORD : {pswrd}"))
                print(MENU(f"PACKAGE : {pkg}"))
                print(MENU(f"INSTALLATION DATE : {inst_date}"))
                
                d=input('CONFIRM DATA [Y/N]: ')
                if d.strip().capitalize() == 'Y':
                    break
                cnf=input(MENU('EXIT ADD USER? [Y/N]'))
                if cnf.strip().capitalize() =="Y":

                    return  0

          
            cx = sqlite3.connect(database)
            cu = cx.cursor()
            cu.execute(f'INSERT INTO account values("{acc}","{name}","{phne}",{pkg},"{usernm}","{pswrd}","{inst_date}",0)')
            cu.execute('SELECT * FROM contacts ORDER BY cid desc limit 1')
            cid=str(int(cu.fetchone()[0]) + 1)
            cu.execute(f'INSERT INTO contacts values({cid},"{acc}","{phne}")')

            pkg_type=cache_package[cache_account[acc]["package"]]['type']
            if pkg_type == 'hotspot':
                hermes.ssh_command(f'ip hotspot user add comment="{name}" name="{usernm}" password="{pswrd}" profile="{mikrotik_profs[int(pkg)]}"  server=hs-new_wingu limit-uptime=5m ')
            elif pkg_type == 'pppoe':
                hermes.ssh_command(f'ppp secret add comment="{name}" name="{usernm}" password="{pswrd}" profile="{mikrotik_profs[int(pkg)]}"  service=ppppoe ')

            cx.commit()
            cx.close()
            return 1
        except Exception as e:
            print(RED('UNABLE TO ADD USER: '+str(e)))
            log('UNABLE TO ADD USER: '+str(e))
            cx.close()
            return 0    
        
    def status():
        try: 
            ls=[]
            usls=list(cache_sessions.keys())
            for c in usls:
                print(f'{cache_sessions[c]["start date"]}/{cache_sessions[c]["start time"]}')
                ls.append(f'{account_nme[c]}[{c}] {cache_sessions[c]["start date"]}/{cache_sessions[c]["start time"]} => {cache_sessions[c]["end date"]}/{cache_sessions[c]["end time"]}')
            g=menu(ls)-1

            print(GREEN(cache_account[usls[g]]))
            return 1

        except Exception as e:
            print(RED('UNABLE TO GET USER STATUS: '+str(e)))
            log('UNABLE TO GET USER STATUS: '+str(e))
            
            return 0  
    
    def session_edit():
        try:
            cx = sqlite3.connect(database)
            cu = cx.cursor()
            cu.execute('Select * FROM sessions WHERE status = "active"')
            dt=cu.fetchall()
            SESS={}
            for d in dt:
                SESS[d[1]]={"sid":d[0],
                            "start date":d[3],
                            "start time":d[4],
                            "end date":d[5],
                            "end time":d[6],
                            "desc":d[2]}
            ac_users=[]#user account no
            users_ls=[]
            ac_users=list(SESS.keys())
            for us in ac_users:
                users_ls.append(f"{account_nme[us]} [{us}]")
            ot=menu(users_ls)
            ot=ot-1
            if ot == -1:
                print('EXITING SESSION EDIT:')
                return 0
            acno=ac_users[ot]
            while 1:
                sd=input(f'Input start date [{SESS[acno]["start date"]}]: ')
                if sd == '':
                    sd=SESS[acno]["start date"]
                #print(sd)
                st=input(f'Input start time [{SESS[acno]["start time"]}]: ')
                if st == '':
                    st=SESS[acno]["start time"]
                #print(st)
                et=input(f'Input end time [{SESS[acno]["end time"]}]: ')
                if et == '':
                    et=SESS[acno]["end time"]
                #print(et)
                ed=input(f'Input end date [{SESS[acno]["end date"]}]: ')
                if ed == '':
                    ed=SESS[acno]["end date"]
                #print(ed)
                
                print(MENU(f'CONFIRM THE FOLLOWING DATA:\n  start date : {sd}\n start time = {st}\n end date = {ed}\n end time = {et}\n Profile = {SESS[acno]["desc"]+"[edited]"}\n'))
                cnf=input(' CONFIRM [Y/N]: ')
                if cnf.strip().capitalize() == 'Y':
                    print('confirmed')
                    break
                else:
                    cnf_e=input(f'DO YOU WANT TO EXIT? [Y/N]')
                    if cnf_e.strip().capitalize() == 'Y':
                        return 0
            log(f'session edited with the following data: :\n  start date : {sd}\n start time = {st}\n end date = {ed}\n end time = {et}\n Profile = {SESS[acno]["desc"]+"[edited]"}\n')
            cu.execute(f'UPDATE sessions set "start date" = "{sd}" WHERE sid = {SESS[acno]["sid"]}')
            cu.execute(f'UPDATE sessions set "end date" = "{ed}" WHERE sid = {SESS[acno]["sid"]}')
            cu.execute(f'UPDATE sessions set "start time" = "{st}" WHERE sid = {SESS[acno]["sid"]}')
            cu.execute(f'UPDATE sessions set "end time" = "{et}" WHERE sid = {SESS[acno]["sid"]}')
            cu.execute(f'UPDATE sessions set "profile" = "{SESS[acno]["desc"]+"[edited]"}" WHERE sid = {SESS[acno]["sid"]}')

            cx.commit()
            cx.close()

            print('pause')
            
        except Exception as e:
            print(RED('UNABLE TO GET USER SESSION EDIT: '+str(e)))
            log('UNABLE TO GET USER SESSION EDIT: '+str(e))
            cx.close()
            return 0 
    
    def compensation():
        try:
            usrs=list(account_nme.keys())
            accomp=[]
            for x in usrs:
                accomp.append(f'{account_nme[x]} [{x}]')
            print(MENU('SELECT ACCOUNT:'))
            i = menu(accomp) -1

            d = input(f'Insert hours to compensate {accomp[i]}: ')
            descr = input('Input reason for compensation: ')

            cx = sqlite3.connect(database)
            cu = cx.cursor()
            cu.execute(f'SELECT package FROM account WHERE acc = "{usrs[i]}"')
            pkg=cu.fetchall()[0][0]
            
            cu.execute(f'SELECT days,price FROM package WHERE pno = {int(pkg)}')
            dp=cu.fetchall()[0]
            days=dp[0]
            price=dp[1]

            comp_amnt=(price * int(d))/(days * 24)
            
            conf=input(MENU(f'CONFIRM THE FOLLOWING: \n account : {accomp[i]}\n hours : {d}\n time value : {comp_amnt}\n [Y/N]'))
            if not conf.strip().capitalize() == 'Y':
                print('EXITING COMPENSATION...')
                return 0



            cu.execute('SELECT * FROM finances ORDER BY fid desc limit 1')
            fid=str(int(cu.fetchone()[0]) + 1)

            cu.execute(f'INSERT INTO finances VALUES({fid},"{str(usrs[i])}",{str(comp_amnt)},0,"{descr}","{str(tme())}")')
            cu.execute(f'SELECT balance FROM account WHERE acc = "{usrs[i]}"')
            bl=cu.fetchall()[0][0]

            cu.execute(f'UPDATE account SET balance = {bl+comp_amnt} WHERE acc = "{usrs[i]}"')

            hermes.session_monitor(usrs[i])

            
            return 1
            
        except Exception as e:
            print(RED(f'ERROR RUNNING COMPENSATIONS: [{str(e)}]'))

    def startup():#what to do when the program first runs
        try:
            print('\033c', end='')
            print(lg)
            print(GREEN(f'{tme()}HERMES WINGU SERVICE STARTUP \n '))
            log('HERMES WINGU SERVICE STARTUP') 

            #check if initialisation is required
            #hermes.initial()

            #1.check if sql and log file exist is available
            try:
                #create log file if it does not exist
                if not os.path.exists(log_file):
                    print(RED(f'LOG FILE DOES NOT EXIST AT {log_file}'))
                    with open(log_file,'w') as file:
                        file.write(f'LOG FILE CREATED ON {tme()}')
                    print(GREEN(f'LOG FILE SUCCESSFULY CREATED AT {current_directory}'))

                #check database
                if not os.path.exists(database):
                    print(f'DATABASE FILE NOT FOUND AT {database}. Cannot proceed.')
                    sys.exit()

                if not cache() :
                    print("cache failed")

                cx = sqlite3.connect(database)
                cu = cx.cursor()
                cu.execute('Select * FROM account')
                dt=cu.fetchall()
                for l in dt:
                    accnt=l[0]
                    nme=l[1]
                    account_nme[accnt]=nme
                print(GREEN(f'{tme()} {database} SQL SERVER AVAILABLE'))
                cx.close()
            except Exception as e:
                print(f'{tme()}ERROR. SQL SERVER UNREACHABLE')
                sys.exit() #EXIT PROGRAM

            #2. RUN SESSION MONITOR TO DISCONNECT ANY UNAUTHORISED USERS
            print('Loading....')
            hermes.session_monitor()

            #3. MIKROTIK ACTIVE CHECKER

            #ssh_otp=hermes.ssh_command('ip hotspot user print detail').strip().split(';;;')

            '''onl_lst=[]
            otp=hermes.dbcommunication('select username,acc from account')
            for c in otp:
                ssh_otp=hermes.ssh_command(f'ip hotspot user print detail where name="{c[0]}"')
                if not 'limit-uptime' in ssh_otp:
                    onl_lst.append(c[1])
                    #print(ssh_otp)
                    #print('*'*50)
                    #with open ('test.txt','a') as e:
                   #      e.write(c[0]+ssh_otp+'\n'+'*'*50)

            #print(onl_lst)
            print('\n\n')
            for a in onl_lst:
                if not a in cache_sessions.keys():
                     print(RED(f'User {account_nme[a]} is not disabled yet has no active session'))
            #with open('test.txt','w') as f:
            #     f.write(ssh_otp)
            print('\n\n')'''

            return 1
                    
        except Exception as e:
            print(RED(f'{tme()}FAILED RUNNING STARTUP. ERROR: {str(e)}'))
            log(f'{tme()}FAILED RUNNING STARTUP. ERROR: {str(e)}')
            return 0
    
    def manual():
        try:
            while 1:
                d=input('>>>')
                print(d)
                if d.strip().capitalize()=='Exit':
                    break

                d_out=hermes.dbcommunication(d)
                d_type=type(d_out)
                ln=[]
                if d_type==type(ln):
                    for d_gp in d_out:
                        print(d_gp)
                else:
                    print(d_out)
            print(GREEN("exiting manual.cli"))
            return 1

        except Exception as e:
            print(RED(f'{tme()}FAILED RUNNING MANUALLY. ERROR: {str(e)}'))
            log(f'{tme()}FAILED RUNNING MANUALLY. ERROR: {str(e)}')
            return 0
        
    def run():
        try:
            cache()
            SCHEDULED_SESSIION_DISSCONNECT=[]
            cx = sqlite3.connect(database)
            cu = cx.cursor() 
            cu.execute('SELECT * FROM sessions WHERE status = "active"')
            OUTPT=cu.fetchall()
            cx.close()
            
            if not len(OUTPT) == 0:
                print("\n"+tme()+'ACTIVE SESSIONS: ')
                for line in OUTPT:
                    print(MENU(f'   {account_nme[line[1]]} => {line[5]} / {line[6]}'))
                    SCHEDULED_SESSIION_DISSCONNECT.append(line[5]+'|'+line[6])        
                
                #print(tme()+'A list of session expieries has been created: '+ MENU(str(SCHEDULED_SESSIION_DISSCONNECT)))
            print('\n\n')

            if len(SCHEDULED_SESSIION_DISSCONNECT) >= 1:

                print(GREEN(f'{tme()} RUNNING AUTO SESSION MONITOR.SERVICE.'))
                '''
                dte_lst=SCHEDULED_SESSIION_DISSCONNECT[-1].split('|')
                next_expiery = datetime.combine(datetime.strptime(dte_lst[0], "%d-%b-%Y").date(), datetime.strptime(dte_lst[1], "%I:%M %p").time())
                '''
                # Convert each date string in the list to a datetime object
                date_objects = [datetime.strptime(date, '%d-%b-%Y|%I:%M %p') for date in SCHEDULED_SESSIION_DISSCONNECT]
                smallest_date = min(date_objects)
                dte_lst=str(smallest_date.strftime('%d-%b-%Y|%I:%M %p')).split('|')
                next_expiery = datetime.combine(datetime.strptime(dte_lst[0], "%d-%b-%Y").date(), datetime.strptime(dte_lst[1], "%I:%M %p").time())

                print(MENU(f"Next disconnection {next_expiery}"))
                print('To exit loop, press CTRL+C')
                while 1:
                    time.sleep(3)
                    if datetime.now()>= next_expiery:#IF NEXT EXPIERY HAS REACHED
                        print(MENU(f'{tme()} Internal system interupt. Exiting monitor.service to check active sessions...'))
                        hermes.session_monitor()
                        index_of_smallest = date_objects.index(smallest_date)

                        # Remove the smallest date from the original list
                        SCHEDULED_SESSIION_DISSCONNECT.pop(index_of_smallest)
                        print(GREEN(f'{tme()} SUCCESSFULLY UPDATED SESSION....'))
                        break
            
            else:
                print(MENU(F'{tme()}NO SCHEDULED DISCONNECTION. MOVING TO MENU.....'))
                main()
            return 1

        except KeyboardInterrupt:
            print("\nEXITING MONITOR.SERVICES. OPENING MENU.....\n\n")
            main()
        except Exception as e:
            log('ERROR RUNNING HERMES: '+str(e))
            print(RED('ERROR RUNNING HERMES: '+str(e)))

    def initial():
        try:
            dir=os.listdir(current_directory)
            print(GREEN('INITIAL STARTUP OF THE HERMES'))

            #create input file
            if not input_fl in dir:
                with open(input_fl,'w')as init:
                    init.write('>>>>FILL IN THE FILLOWING DATA<<<<\n')
                    init.write('+'+'-'*48+'+\n')
                    init.write("| DATABASE NAME         |     DATABASE.db        |\n")
                    init.write('+'+'-'*48+'+\n')
                    init.write("| LOG FILE NAME         |    log_test.txt        |\n")
                    init.write('+'+'-'*48+'+\n')
                    init.write("| MIKROTIK IP           |    192.168.88.1        |\n")
                    init.write('+'+'-'*48+'+\n')
                    init.write("| MIKROTIK USERNAME     |    USERNAME            |\n")
                    init.write('+'+'-'*48+'+\n')
                    init.write("| MIKROTIK PASSWORD     |    PASSWORD            |\n")
                    init.write('+'+'-'*48+'+\n')
                
                print(RED('INPUT FILE COULD NOT BE FOUND. A FILE HAS BEEN CREATED '),end='')
                print(f"{RED('AT')} {MENU(current_directory)} {RED('NAMED')} {MENU(input_fl)}{RED('. FILL IT WITH APPROPRIATE DATA BEFORE PROCEEDING ')}")
                cnf=input('Proceed [Y/N]: ')
                if not cnf.strip().capitalize()=='Y':
                    print(RED('INITIALISATION BROKEN. EXITING...'))
                    sys.exit()
            
            with open (os.path.join(current_directory, input_fl),'r') as infl:
                ld=infl.readlines()

            database_name=ld[2].split('|')[2].strip()
            log_file_name=ld[4].split('|')[2].strip()
            mk_ip = ld[6].split('|')[2].strip()
            mk_username = ld[8].split('|')[2].strip()
            mk_password = ld[10].split('|')[2].strip()
            database = os.path.join(current_directory, database_name) 
            log_file= os.path.join(current_directory, log_file_name)

            #create log file
            if not log_file in dir:
                print('CREATING LOG FILE...',end='')
                with open(log_file,'w') as d:
                    d.write(' ')
                print(GREEN('DONE'))

            #create database
            if not database in dir:
                print('CREATING DATABASE...',end='')
                with open('init.txt','r') as e:
                    in_dt=e.read().strip().split(';')

                cx = sqlite3.connect(database)
                cu = cx.cursor()
                for d in in_dt:
                    cu.execute(d)

                cx.commit()
                cx.close()
                print(GREEN('DONE'))
            
            database = os.path.join(current_directory, database_name) 
            log_file= os.path.join(current_directory, log_file_name)
            
            while 1:#add package
                print(MENU("Lets create first package. "))
                name=input(MENU('Input package name: '))
                speed_sel = input(MENU('Input speed: [int] '))
                try:
                    speed=int(speed_sel)
                except:
                    print(RED("invalid speed"))
                    continue

                days_sel=input(MENU('Input number of days per subscription: [int] '))
                try:
                    days=int(days_sel)
                except:
                    print(RED("invalid days"))
                    continue
                users_sel=input(MENU('Input maximum users per connection[HOTSPOT ONLY]: '))
                try:
                    users=int(users_sel)
                except:
                    print(RED("invalid users"))
                    continue
                price=input(MENU('Input price per subscription: [int] '))

                p_type=input(MENU('Select package type [HOTSPOT/PPPOE]: '))

                if p_type.strip().capitalize().split()=='P':
                    p_type='pppoe'
                else:
                    p_type='hotspot'

                cnf=input(RED(f'CONFIRM THE PRVIDED DATA: \n    PACKAGE NAME: {name}\n  PACKAGE SPEED: {speed}\n    PACKAGE DAYS: {days}\n  MAX USERS: {users}\n    PRICE: {price}\n   PACKAGE: {p_type}\n\n>>>[Y/N] '))
                
                if cnf.strip().capitalize()=='Y':
                    if not hermes.add_pkg(name,speed,days,users,price,p_type) == 1:
                        print(RED('FAILED TO ADD PACKAGE'))
                    else:
                        break
                
                cnf=input('RETRY? [Y/N] ')
                if cnf.strip().capitalize()=='N':
                    print(RED('Failed package add. EXITING...'))
                    sys.exit()

            


            print('INITIALISATION COMPLETED')
            return 1
        
        
        except Exception as e:
            print('FAIL INITIALISING WINGU ' + str(e))
            #log('FAIL INITIALISING WINGU')
            return 0

                   
def main():
    menu_list=['ADD USER','COMPENSATION','ADD USER PAYMENT','SESSION EDIT','SWITCH TO AUTO_MONITOR','STATUS','MANUAL CLI','EXIT']
    a=str(menu(menu_list))
    if a=='1':#add user
        print(GREEN('SWITCHING TO ADD USER'))
        hermes.add_user()
    elif a == '2':#compensation
        print(GREEN(f'RUNNING COMPENSATION...'))
        hermes.compensation()
    elif a=='3':
        def_date_lst=time.ctime().strip().split(' ')
        def_date=f'{def_date_lst[2]}-{def_date_lst[1]}-{def_date_lst[4]}'
        print("RUNNING PAYMENT MANAGER SERVICE...\n\n")
        while 1:
            code=input('INPUT TRANSACTION CODE: ')
            ammount=input('INPUT AMOUNT: ')
            source=input('INPUT SOURCE: ')
            date=input(f'INPUT DATE [{def_date}] : ')
            if date == '':
                date= str(def_date)
            timet=input('INPUT TIME[hh:mm PM/AM]: ')
            conf=input(MENU(f'\nCODE: {code},\n  AMOUNT: {ammount},\n  SOURCE : {source},\n   DATE : {date},\n    TIME: {timet}\n ')+' CONFIRM DATA Y/N: ')
            
            if conf.strip().capitalize()=='Y':
                hermes.payments(code,ammount,source,date,timet)
                break
            else:
                cn=input(MENU('DO YOU WANT TO EXIT [Y/N]?'))
                if cn.strip().capitalize()=='Y':
                    break

    elif a=='4':
        print(GREEN(f'RUNNING SESSION EDIT...'))
        hermes.session_edit()
    elif a=='5':
        print(GREEN('SWITCHING BACK TO AUTO'))
        hermes.run()
    elif a=='6':
        print(GREEN('CURRENT SESSIONS'))
        hermes.status()
    elif a=='7':
        print(GREEN('SWITCHING TO MANUAL CLI'))
        hermes.manual()
    elif a=='8':
        print(f'{tme()}EXITING WINGU.SERVICES')
        log('USER REQUEST EXIT FROM SERVICE')
        sys.exit()

    print('SWITCHING TO AUTO SESSION MONITOR')
    hermes.run()

#################################################################
clear_terminal()


print (lg)

current_directory = os.getcwd()  # Get the current working directory
dir=os.listdir(current_directory)
if not os.path.join(current_directory, input_fl) in dir:
    print(RED('INPUT FILE NOT FOUND'))
    hermes.initial()


#VARIABLES FETCH
with open (os.path.join(current_directory, input_fl),'r') as infl:
    ld=infl.readlines()

database_name=ld[2].split('|')[2].strip()
log_file_name=ld[4].split('|')[2].strip()
mk_ip = ld[6].split('|')[2].strip()
mk_username = ld[8].split('|')[2].strip()
mk_password = ld[10].split('|')[2].strip()
database = os.path.join(current_directory, database_name) 
log_file= os.path.join(current_directory, log_file_name)


# Call the function to clear the terminal screen
clear_terminal()

#print('k')
hermes.startup()
#infinite loop
while 1:
	hermes.run()
