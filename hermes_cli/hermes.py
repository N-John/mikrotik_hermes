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
import random
#import threading
#import msvcrt

#VARIABLES
input_fl='variables.txt'
running = True



#CACHE
cache_account={}
cache_contacts={}
cache_finances={}
cache_package={}
cache_payments={}
cache_sessions={}
cache_pppoe={}

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
LAST MODIFIED: 24-July-2024
    '''


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

def log(dat:str):
    with open (log_file,'a') as log:
        log.write(f'\n {tme()} {dat}')
    #print(f'{tme()} {dat}') #comment this line to reduce verbose

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
        global cache_pppoe

        cache_account={}
        cache_contacts={}
        cache_finances={}
        cache_package={}
        cache_payments={}
        cache_sessions={}
        cache_pppoe={}

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
        print('#'*10,end='')
        #pppoe acccount cache
        cu.execute('SELECT * FROM PppoeAccounts')
        OUTPT=cu.fetchall()
        for data in OUTPT:
            cache_pppoe[data[0]]={"name"        :data[1],
                                "phone"         :data[2],
                                "location"      :data[3],
                                "ip"            :data[4],
                                "username"      :data[5],
                                "password"      :data[6],
                                "package"       :data[8],
                                "creation date" :data[7],
                                "balance"       :data[9]
                                }
        
        print(f"{'#'*10}] 100%\033[0m")
        cx.close()

        return 1
    except Exception as e:
        print(RED('#'*10))
        print(RED(f'USER CACHE FAIL: {str(e)}'))
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

class _admin:
    def accounting():
        try:
            tt=time.ctime().split(' ')
            while 1:
                START_DATE=input('INPUT START DATE[1-Jan-2024]: ').strip()
                if START_DATE.capitalize() == '':
                    START_DATE='1-Jan-2024'

                START_TIME=input('INPUT START TIME[12:00 AM]: ').strip()
                if START_TIME.capitalize() == '':
                    START_TIME='12:00 AM'

                END_DATE=input(f'INPUT END DATE[{tt[-3]}-{tt[1]}-{tt[-1]}]: ').strip()
                if END_DATE.capitalize()=='':
                    END_DATE=f'{tt[-3]}-{tt[1]}-{tt[-1]}'
                
                END_TIME=input(f'INPUT END TIME[11:59 PM]: ').strip()
                if END_TIME.capitalize()=='':
                    END_TIME='11:59 PM'
                print(f'START DATE: {START_DATE}\nSTART TIME: {START_TIME}\nEND DATE: {END_DATE}\nEND TIME: {END_TIME}')
                cnf=input('CONFIRM[Y/N]: ').strip()
                if cnf.capitalize()=='Y':
                    break
                else:
                    return 1

            cx = sqlite3.connect(database)
            cu = cx.cursor()
            cu.execute('SELECT * FROM payments')
            OUTPT=cu.fetchall()
            cx.close()
            total = 0
            c=0
            accounting_dict={}
            for line in OUTPT:
                try:
                    start_combined_datetime = datetime.combine(datetime.strptime(START_DATE, "%d-%b-%Y").date(), datetime.strptime(START_TIME, "%I:%M %p").time())
                    end_combined_datetime = datetime.combine(datetime.strptime(END_DATE, "%d-%b-%Y").date(), datetime.strptime(END_TIME, "%I:%M %p").time())
                    payment_combined_datetime = datetime.combine(datetime.strptime(line[5], "%d-%b-%Y").date(), datetime.strptime(line[6], "%I:%M %p").time())
                    if payment_combined_datetime >= start_combined_datetime and payment_combined_datetime <= end_combined_datetime:
                        #print(line)
                        ak=list(accounting_dict.keys())
                        if line[1] in ak:
                            a_total=accounting_dict[line[1]]["total"]+line[3]
                            accounting_dict[line[1]]["total"]=a_total
                            a_count=accounting_dict[line[1]]["count"]+1
                            accounting_dict[line[1]]["count"]=a_count
                        else:
                            accounting_dict[line[1]] = {
                                'total': line[3],
                                'count': 1
                            }
                        total = total + line[3]
                        c=c+1
                except:
                    print(line[5]+'#'+line[6])
                    continue
            
            print(f'+{"-"*10}+{"-"*35}+{"-"*7}+{"-"*15}+')
            print(f'|ACCOUNT{" "*3}|NAME{" "*31}| COUNT |AMOUNT{" "*9}|')
            print(f'+{"-"*10}+{"-"*35}+{"-"*7}+{"-"*15}+')
            for acc in accounting_dict:
                print(f'|{acc}{" "*(10-len(acc))}',end='')
                print(f'|{cache_account[acc]["name"]}{" "*(35-len(cache_account[acc]["name"]))}',end='')
                print(f'|{accounting_dict[acc]["count"]}{" "*(7-len(str(accounting_dict[acc]["count"])))}',end='')
                print(f'| Ksh {accounting_dict[acc]["total"]}{" "*(10-len(str(accounting_dict[acc]["total"])))}|')
                
                #print(f'|{acc}{" "*(10-len(acc))}|{accounting_dict[acc]["count"]}{" "*(5-len(str(accounting_dict[acc]["count"])))}| Ksh {accounting_dict[acc]["total"]}{" "*(10-len(str(accounting_dict[acc]["total"])))}|')
            print(f'+{"-"*10}+{"-"*35}+{"-"*7}+{"-"*15}+')
            print(f'=> TOTAL ACCOUNTS: {len(accounting_dict.keys())}')
            print(f'=> TOTAL PAYMENTS: {c}')
            print(f'=> TOTAL AMOUNT: Ksh {total}')
            print('_'*57)
           
        except Exception as e:
            print(RED(f'FAIL ADMIN ACCOUNTING WITH ERROR: [{str(e)}]'))

    def user_man():
        try:
            pass
        except Exception as e:
            print(RED(f'FAIL ADMIN USER_MAN WITH ERROR: [{str(e)}]'))

class remoSys():
    def packageFetch():
        functOut=hermes.ssh_command(['ppp profile print','ip hotspot user profile print'])
        datp=str(functOut[0]).strip().split('\r\n\r\n')
        rempkg={}
        c=0
        for datl in datp:
            try:
                pnames=datl.strip().split('name="')[1].split('"')[0]
                if pnames== 'default':
                    continue
                rempkg[c]={"name":pnames,
                           "pkg_type":'pppoe'}
                c+=1
            except:
                pass
        dath=str(functOut[1]).split('\r\n\r\n')
        #print(dat)
        for datl in dath:
            try:
                pnames=datl.strip().split('name="')[1].split('"')[0]
                if pnames== 'default':
                    continue
                rempkg[c]={"name":pnames,
                           "pkg_type":'hotspot'}
                c+=1
            except:
                pass

        return rempkg

class hermes:
    def ssh_command(cmds:list):
        # Establish SSH connection to the MikroTik router
        try:
            output=[]
            if len(cmds)<1:
                return 0
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=mk_ip, username=mk_username, password=mk_password)
            print(GREEN(f"{tme()}CONNECTED TO SERVER VIA SSH"))
            
            for cmd in cmds:
                print(f'Running command [{cmd}]')
                stdin, stdout, stderr = ssh_client.exec_command(f'log warning "auto running command {cmd}"')
                stdin, stdout, stderr = ssh_client.exec_command(cmd)
                output.append(stdout.read().decode('utf-8'))
            #print(MENU(output))
            ssh_client.close()
            return output

        except paramiko.AuthenticationException:
            print(RED(f"{tme()}Authentication to router FAIL, please check your credentials."))
            log('ERROR CONNECTING TO SSH SERVER: AUTHENTICATION FAIL')
            return f"Authentication FAIL, please check your credentials: {ssh_err}"
        
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
            #print(f'Running db communication command [{comm}]')
            cx = sqlite3.connect(database)
            cu = cx.cursor()
            cu.execute(comm)
            OUTPT=cu.fetchall()
            cx.commit()
            cx.close()
            #print(OUTPT)
            return OUTPT

        except Exception as e:
            print(RED(f'FAIL SQL: {str(e)}'))
            return 0

    def initial():
        try:
            dir=os.listdir(current_directory)
            print(GREEN('INITIAL STARTUP OF THE HERMES'))

            #create input file
            if not input_fl in dir:
                with open(input_fl,'w')as init:
                    init.write('>>>>FILL IN THE FILLOWING DATA<<<<\n')
                    init.write('+'+'-'*48+'+\n')
                    init.write("| DATABASE NAME         |     DATABASE.sqlite3        |\n")
                    init.write('+'+'-'*48+'+\n')
                    init.write("| LOG FILE NAME         |       log.txt          |\n")
                    init.write('+'+'-'*48+'+\n')
                    init.write("| MIKROTIK IP           |     192.168.88.1       |\n")
                    init.write('+'+'-'*48+'+\n')
                    init.write("| MIKROTIK USERNAME     |       USERNAME         |\n")
                    init.write('+'+'-'*48+'+\n')
                    init.write("| MIKROTIK PASSWORD     |       PASSWORD         |\n")
                    init.write('+'+'-'*48+'+\n')
                
                print(RED('INPUT FILE COULD NOT BE FOUND. A FILE HAS BEEN CREATED '),end='')
                print(f"{RED('AT')} {MENU(current_directory)} {RED('NAMED')} {MENU(input_fl)}{RED('. FILL IT WITH APPROPRIATE DATA BEFORE PROCEEDING ')}")
                cnf=input('Proceed [Y/N]: ')
                if not cnf.strip().capitalize()=='Y':
                    print(RED('INITIALISATION BROKEN. EXITING...'))
                    sys.exit()
            
            with open (os.path.join(current_directory, input_fl),'r') as infl:
                ld=infl.readlines()

            global mk_ip
            global mk_username
            global mk_password
            global database
            global log_file

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
            print('Checking if Connection to router is possible...')


            try:
                print('Checking on router profiles...')
                remotePackages=remoSys.packageFetch()
                print(f'fnd {remotePackages}')
                confer=input(f'Found {len(remotePackages)} packages on router. Do you want to add them [Y/N]? ')
                if confer.capitalize()=='Y':
                    c=0
                    cx = sqlite3.connect(database)
                    cu = cx.cursor()
                    while 1:
                        for rp in list(remotePackages.keys()):
                            pname=remotePackages[rp]['name']
                            ptype=remotePackages[rp]['pkg_type']
                            print(f'\n {"*"*10} {pname} [{ptype}] {"*"*10}')

                            while 1:
                                speed_sel = input(MENU(f'       Speed [int]: '))
                                try:
                                    speed=int(speed_sel)
                                    break
                                except:
                                    print(RED("invalid speed"))
                                    continue
                            while 1:
                                days_sel=input(MENU(f'      Number of days per subscription [int]: '))
                                try:
                                    days=int(days_sel)
                                    break
                                except:
                                    print(RED("invalid days"))
                                    continue
                            if ptype == 'hotspot':
                                while 1:
                                    users_sel=input(MENU(f'     Maximum users per connection [int]: '))
                                    try:
                                        users=int(users_sel)
                                        break
                                    except:
                                        print(RED("invalid users"))
                                        continue
                            
                            while 1:
                                price=input(MENU(f'     Price per subscription [int]: '))
                                try:
                                    users=int(price)
                                    break
                                except:
                                    print(RED("invalid Price"))
                                    continue

                            cu.execute(f'INSERT INTO package VALUES({c},"{pname}",{speed},{days},{users},{price},"{ptype}")')
                            c+=1
                            

                            print("\n")
                        break
                    cx.commit()
                    cx.close()
                    cache()
                    exconf=input("Do you want to add more packages[Y/N]? ")
                    if exconf.strip().capitalize()=='N':
                        print('INITIALISATION COMPLETED')
                        return 1

            except Exception as e:
                cx.commit()
                cx.close()
                print(RED(f'Failed To fetch packages from router {str(e)}'))
            
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

                cnf=input(GREEN(f'CONFIRM THE PRVIDED DATA: \n    PACKAGE NAME: {name}\n  PACKAGE SPEED: {speed}\n    PACKAGE DAYS: {days}\n  MAX USERS: {users}\n    PRICE: {price}\n   PACKAGE: {p_type}\n\n>>>[Y/N] '))
                
                if cnf.strip().capitalize()=='Y':
                    while 1:
                        try:
                            cx = sqlite3.connect(database)
                            cu = cx.cursor()
                            pno=len(cache_package.keys())+1
                            cu.execute(f'INSERT INTO package VALUES({pno},"{name}",{speed},{days},{users},{price},"{p_type}")')
                            cx.commit()
                            cx.close()
                            if p_type == 'hotspot':
                                hermes.ssh_command([f'ip hotspot user profile add name="{name}" shared-users="{users}" rate-limit="{speed}M/{speed}M"'])
                            elif p_type == 'pppoe':
                                hermes.ssh_command([f'ppp profile add name="{name}" rate-limit="{speed}M/{speed}M"'])
                            print(GREEN('INITIALISATION COMPLETED'))
                            return 1
                        except Exception as e:
                            print(RED(f'ERROR ADDING PACKAGE : {e}'))
                            cnf=input('RETRY? [Y/N] ')
                            if cnf.strip().capitalize()=='N':
                                print(RED('FAIL package add. EXITING...'))
                                sys.exit()
                            else:
                                break

                   
            print('INITIALISATION COMPLETED')
            return 1
        
        except Exception as e:
            print('FAIL INITIALISING WINGU ' + str(e))
            sys.exit()
            #log('FAIL INITIALISING WINGU')
            return 0

    def payments(code:str,amount:str,source:str,date:str,time_tm:str):
        try:
            acc_type=''#hotspor or pppoe
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

                    for cp in cache_pppoe:
                        ld_list.append(f"{cache_pppoe[cp]['name']} : {cp}")

                    otp=menu(ld_list)-1
                    cnf = input(f'CONFIRM {ld_list[otp]} [Y/N] ')
                    if cnf.strip().capitalize() == 'Y':
                        
                        print(GREEN('CONFIRMED..'))
                        acc=ld_list[otp].split(':')[1].strip()
                        if 'Wn' in acc:
                            phone=cache_pppoe[ld_list[otp].split(':')[1].strip()]["phone"]
                            acc_type='pppoe'
                        elif 'Wp' in acc:
                            phone=cache_account[ld_list[otp].split(':')[1].strip()]["phone"]
                            acc_type='hotspot'


                        cx = sqlite3.connect(database)
                        cu = cx.cursor()
                        cu.execute(f'SELECT cid FROM contacts')
                        cid=str(int(cu.fetchall()[-1][0])+1)
                        cu.execute(f'INSERT INTO contacts VALUES({cid},"{acc}","{source}")')
                        cx.commit()
                        cx.close()
                        print(f'contact added: [{cid},"{acc}","{source}"]')
                    else:
                        print('EXITING....')
                        return 0
                else:
                    print('EXITING...')
                    return 0

            else:
                acc = cache_contacts[source]['account']
                if 'Wn' in acc:
                    acc_type='pppoe'
                else:
                    acc_type='hotspot'

            print(GREEN('Account determined as '+acc))

            cx = sqlite3.connect(database)
            cu = cx.cursor()
            cu.execute(f'SELECT pid FROM payments')
            cache()
            pid=str(len(cache_payments)+1)
            
            cu.execute(f'insert into payments values ({pid},"{acc}","{code}",{amount},"{source}","{date}","{time_tm}")') 
            log(f'insert into payments values ({pid},"{acc}","{code}",{amount},"{source}","{date}","{time_tm}")')
            print('payment values added')
           
            #add to finances 
            print(f"adding to finance for {cache_account[acc]['name']}")
            cu.execute(f'SELECT fid FROM finances')
            fid=str(len(cache_finances)+1)
            cu.execute(f'insert into finances values ({fid},"{acc}",{amount},0.00,"DEPOSIT","{str(tme())}")')
            log(f'insert into finances values ({fid},"{acc}",{amount},0.00,"DEPOSIT","{str(tme())}")')
            cache()

            #ADD MONEY TO USER ACCOUNT
            print(f"Adding money to {cache_account[acc]['name']} account")
            if acc_type == 'hotspot':
                balance=cache_account[acc]['balance'] + int(amount)
                print(f'NEW HOTSPOT BALANCE {balance}')
                cu.execute(f'UPDATE account set balance = {str(balance)} WHERE acc = "{acc}";')
                log(f'UPDATE account set balance = {str(balance)} WHERE acc = "{acc}";')
            elif acc_type == 'pppoe':
                balance=cache_pppoe[acc]['balance'] + int(amount)
                print(f'NEW PPPoE BALANCE {balance}')
                cu.execute(f'UPDATE PppoeAccounts set balance = {str(balance)} WHERE acc = "{acc}";')
                log(f'UPDATE PppoeAccounts set balance = {str(balance)} WHERE acc = "{acc}";')

            #print(f'NEW BALANCE {balance}')
            #cu.execute(f'UPDATE account set balance = {str(balance)} WHERE acc = "{acc}";')
            #log(f'UPDATE account set balance = {str(balance)} WHERE acc = "{acc}";')
            print(GREEN(f'{tme()} USER PAYMENT ADDED WITH VALUES: ({pid},\nname: "{cache_account[acc]["name"]}",\ncode : "{code}",\namount : {amount},\nsource : "{source}",\ndate : "{date}",\ntime : "{time_tm}")'))
            cx.commit()
            cx.close()
            cache()

            if acc_type == 'hotspot':#TO BE REMOVED WITH UPDATE
                hermes.session_monitor(acc)
            return 1
        except Exception as e:
            print(RED(f'FAIL ADD PAY: {str(e)}'))
            log(f'FAIL ADD PAY: {str(e)}')
            cx.close()
            return 0
    
    def session_monitor(sm_acc=None):
        try:
            #check if user has an active session. if so,leave.
            #else, get money from sm_acc and create a new session
            print("RUNNING SESSION MONITOR")
            cx = sqlite3.connect(database)
            cu = cx.cursor()
            print('&&')

            if not sm_acc == None:#if a user is specified, check even they have an inactive session
                #print(f'SPECIAL session monitor for {cache_account[sm_acc]["name"]}')
                print('&&')
                cu.execute(f'SELECT * FROM sessions WHERE acc = "{sm_acc}" AND status = "active"')
                print('&&')
                acc_sess=cu.fetchall()
                print('&&')

                if len(acc_sess) == 0: #if no active session create new session
                    print(f'User {cache_account[sm_acc]["name"]} has no active session.\n Creating session...')
                   
                    PKGU=cache_account[sm_acc]["package"]
                    BALU=cache_account[sm_acc]["balance"]
                    PKG_PRICEU=cache_package[PKGU]["price"]#PRICE OF THE PACKAGE
                    PKG_NAMEU=cache_package[PKGU]["name"]#NAME OF THE PACKAGE
                    days_to_addU=cache_package[PKGU]["days"]#HOW MANY DAYS THE PACKAGE COVERS


                    if BALU >= PKG_PRICEU:#if balance is enough to parchase nxt package
                        #remove money from account
                        cu.execute('SELECT * FROM finances ORDER BY fid desc limit 1')
                        fid=str(len(cache_finances) + 1)
                        cu.execute(f'insert into finances values ({fid},"{str(sm_acc)}",0.00,{str(cache_package[PKGU]["price"])},"{cache_package[PKGU]["name"]} SEBSCRIPTION RENEWAL","{str(tme())}")')
                        log(f'insert into finances values ({fid},"{str(sm_acc)}",0.00,{str(cache_package[PKGU]["price"])},"{cache_package[PKGU]["name"]} SEBSCRIPTION RENEWAL","{str(tme())}")')
                        cache()
                        BALU=BALU-PKG_PRICEU
                        cu.execute(f'UPDATE account set balance = {str(BALU)} WHERE acc = "{sm_acc}"')
                        log(f'UPDATE account set balance = {str(BALU)} WHERE acc = "{sm_acc}"')
                        print(f'{sm_acc} Balance updated to {BALU}')

                        #create next session
                        TME=time.ctime().split(' ')
                        S_DATE=f'{TME[-3]}-{TME[1]}-{TME[-1]}'
                        S_TIME = datetime.strptime(TME[-2], "%H:%M:%S").strftime("%I:%M %p")
                        E_DATE = (datetime.strptime(S_DATE, "%d-%b-%Y") + timedelta(days=days_to_addU)).strftime("%d-%b-%Y")
                        
                        log('SELECT * FROM sessions ORDER BY sid desc limit 1')
                        sid=str(len(cache_sessions) + 1)
                        cu.execute(f'INSERT INTO sessions VALUES({sid},"{sm_acc}","{PKG_NAMEU}","{S_DATE}","{S_TIME}","{E_DATE}","{S_TIME}","active","{str(tme())}")')
                        log(f'INSERT INTO sessions VALUES({sid},"{sm_acc}","{PKG_NAMEU}","{S_DATE}","{S_TIME}","{E_DATE}","{S_TIME}","active","{str(tme())}")')  
                        cx.commit()
                        print(GREEN(f'{tme()}New LOCAL session is created for {cache_account[sm_acc]["name"]} with the following values. ({sid},package : "{PKG_NAMEU}",start date : "{S_DATE}",start time : "{S_TIME}",end date : "{E_DATE}", end time : "{S_TIME}","active")'))

                        if cache_package[cache_account[sm_acc]["package"]]["type"] == 'pppoe':
                            print(MENU(f'CREATING NEW REMOTE PPPoE SESSION FOR {cache_account[sm_acc]["name"]}'))
                            cmd=[f'ppp secret set "{cache_account[sm_acc]["username"]}" disabled=no']
                            hermes.ssh_command(cmd)
                        elif cache_package[cache_account[sm_acc]["package"]]["type"] == 'hotspot':
                            print(MENU(f'CREATING NEW REMOTE HOTSPOT SESSION FOR {cache_account[sm_acc]["name"]}'))
                            cmd=[f'ip hotspot user set "{cache_account[sm_acc]["username"]}" limit-uptime=0']
                            hermes.ssh_command(cmd)      

                    else:
                        print(f'USER {cache_account[sm_acc]["name"]} ACCOUNT BALANCE IS STILL INSUFFICIENT. NO SESSION CREATED') 

                else:
                    print(f'USER {cache_account[sm_acc]["name"]} ALREADY HAS AN ACTIVE SESSION.')           


            cu.execute('SELECT * FROM sessions WHERE status = "active"')           
            active_sess=cu.fetchall()

            for dat in active_sess:#loop through active sessions
                #print(f"{tme()} CHECKING ACTIVE SESSION {str(dat)}")

                #check if session is over
                combined_datetime = datetime.combine(datetime.strptime(dat[5], "%d-%b-%Y").date(), datetime.strptime(dat[6], "%I:%M %p").time())
                if combined_datetime <= datetime.now():
                    #(1) SET THE SESSION TO EXIRED
                    acc_no=dat[1]
                    print(f"SESSION EXPIRED FOR {cache_account[acc_no]['name']}[{acc_no}]")
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
                        fid=str(len(cache_finances) + 1)
                        cu.execute(f'insert into finances values ({str(fid)},"{str(acc_no)}",0.00,{str(PKG_PRICE)},"SEBSCRIPTION RENEWAL","{str(tme())}")')
                        log(f'insert into finances values ({str(fid)},"{str(acc_no)}",0.00,{str(PKG_PRICE)},"SEBSCRIPTION RENEWAL","{str(tme())}")')
                        cache()
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
                        sid=str(len(cache_sessions) + 1)
                        cu.execute(f'INSERT INTO sessions VALUES({sid},"{acc_no}","{PKG_NAME}","{S_DATE}","{S_TIME}","{E_DATE}","{S_TIME}","active","{str(tme())}")')
                        log(f'INSERT INTO sessions VALUES({sid},"{acc_no}","{PKG_NAME}","{S_DATE}","{S_TIME}","{E_DATE}","{S_TIME}","active","{str(tme())}")')
                        print(GREEN(f'{tme()} NEW LOCAL SESSION CREATED FOR {cache_account[acc_no]["name"]} WITH VALUES ({sid},package : "{PKG_NAME}",start date : "{S_DATE}",start time : "{S_TIME}",end date : "{E_DATE}",end time : "{S_TIME}","active","{str(tme())}")'))

                        #enable user on server
                        cu.execute(f'SELECT username FROM account where acc = "{acc_no}"')
                        un=cu.fetchall()[0][0]

                        if cache_package[cache_account[acc_no]["package"]]["type"] == 'pppoe':
                            print(MENU(f'CREATING NEW REMOTE PPPoE SESSION FOR {cache_account[acc_no]["name"]}'))
                            cmd=[f'ppp secret set "{cache_account[acc_no]["username"]}" disabled=no']
                            hermes.ssh_command(cmd)
                        elif cache_package[cache_account[acc_no]["package"]]["type"] == 'hotspot':
                            print(MENU(f'CREATING NEW REMOTE HOTSPOT SESSION FOR {cache_account[acc_no]["name"]}'))
                            cmd=[f'ip hotspot user set "{cache_account[acc_no]["username"]}" limit-uptime=0']
                            hermes.ssh_command(cmd)
                   

                    else:
                        #disable user session
                        print(f'{tme()} USER {cache_account[acc_no]["name"]} DISCONTINUED FROM CONNECTION')
                        un=cache_account[acc_no]["username"]
                        if cache_package[cache_account[acc_no]["package"]]["type"] == 'pppoe':
                            cmd=[f'ppp secret set "{un}" disabled=yes',f'ppp active remove [find name="{un}"]']
                            hermes.ssh_command(cmd)
                        elif cache_package[cache_account[acc_no]["package"]]["type"] == 'hotspot':
                            cmd=[f'ip hotspot user set "{un}" limit-uptime=1s',f'ip hotspot active remove [find name="{un}"]']
                            hermes.ssh_command(cmd)

            cx.commit()
            cx.close()
            print('SESSION MONITOR COMPLETED')
            
        except Exception as e:
            cx.close()
            print(RED(f'FAIL SESSION MONITOR: {str(e)}'))
            log(f'FAIL SESSION MONITOR: {str(e)}')
            return 0

    def add_pkg(name:str,speed:int,days:int,users:str,price:int,p_type):
        try:
            cx = sqlite3.connect(database)
            cu = cx.cursor()
            pno=len(cache_package.keys())+1
            cu.execute(f'INSERT INTO package VALUES({pno},"{name}",{speed},{days},{users},{price},"{p_type}")')
            cx.commit()
            cx.close()
            if p_type == 'hotspot':
                hermes.ssh_command([f'ip hotspot user profile add name="{name}" shared-users="{users}" rate-limit="{speed}M/{speed}M"'])
            elif p_type == 'pppoe':
                hermes.ssh_command([f'ppp profile add name="{name}" rate-limit="{speed}M/{speed}M"'])

        except Exception as e:
            print(RED(f'Package add error: [{str(e)}]'))   

    def add_user():
        try:
            print(MENU('ADDING USER: '))
            def_acc=f'hw{random.randint(1000,9999)}'#random default account
            #def_pkg_no=#Default package no
            def_date_lst=time.ctime().strip().split(' ')
            def_date=f'{def_date_lst[2]}-{def_date_lst[1]}-{def_date_lst[4]}'
            
            while 1:
                acc=input(MENU(f"Input Account no: [{def_acc}]"))
                if acc == '':
                    acc=def_acc

                name=input(MENU("Input the user's name: "))
                
                while 1:
                    try:
                        phne=input(MENU("Input their phone number: "))
                        phne_conf=int(phne)
                        break
                    except:
                        print(RED('Invalid phone number'))

                usernm=input(MENU("Input username: "))
                pswrd=input(MENU("Input password: "))
                inst_date=input(MENU(f"Input installation date: [{def_date}]"))

                if inst_date == '':
                    inst_date=def_date
                
                print(f'Available packages: ')
                for pno in list(cache_package.keys()):
                    print(f"    {pno} -> {MENU(cache_package[pno]['name'])}")

                #if you have a selected default package
                '''pkg = input(MENU(f'Select package: [{cache_package[def_pkg_no]["name"]}] => '))
                if pkg =='':
                    pkg = str(def_pkg_no)'''

                pkg = input(MENU(f'Select package: [int]=> '))
                pkg_type=cache_package[int(pkg)]['type']
                pkg_name=cache_package[int(pkg)]['name']
                print('\n'+'*'*20)

                print(MENU(f"ACCOUNT : {acc}"))
                print(MENU(f"NAME : {name}"))
                print(MENU(f"PHONE : {phne}"))
                print(MENU(f"USERNAME : {usernm}"))
                print(MENU(f"PASSWORD : {pswrd}"))
                print(MENU(f"PACKAGE : {pkg_name}"))
                print(MENU(f"TYPE: {pkg_type}"))
                print(MENU(f"INSTALLATION DATE : {inst_date}"))
                print('\n'+'*'*20)

                d=input('CONFIRM DATA [Y/N]: ')
                if d.strip().capitalize() == 'Y':
                    break
                cnf=input(MENU('EXIT ADD USER? [Y/N]'))
                if cnf.strip().capitalize() =="Y":
                    return  0

            cx = sqlite3.connect(database)
            cu = cx.cursor()
            cmd=[]
            if pkg_type == 'hotspot':
                cu.execute(f'INSERT INTO account values("{acc}","{name}","{phne}",{pkg},"{usernm}","{pswrd}","{inst_date}",0)')
                cid=len(cache_contacts)+1
                cu.execute(f'INSERT INTO contacts values({cid},"{acc}","{phne}")')
                cmd.append(f'ip hotspot user add comment="{name}" name="{usernm}" password="{pswrd}" profile="{pkg_name}"  server=hs-new_wingu limit-uptime=5m ')
                
            elif pkg_type == 'pppoe':
                location=input('Input location: ').strip()
                ip=input('Input remote ip: ').strip().strip()
                cu.execute(f'INSERT INTO PppoeAccounts values("{acc}","{name}","{phne}","{location}","{ip}","{usernm}","{pswrd}","{inst_date}",{pkg},0)')
                cid=len(cache_contacts)+1
                cu.execute(f'INSERT INTO contacts values({cid},"{acc}","{phne}")')
                cmd.append(f'ppp secret add comment="{name}" name="{usernm}" password="{pswrd}" profile="{pkg_name}"  service=pppoe ')
            cx.commit()
            cx.close()

            hermes.ssh_command(cmd)

            
            return 1
        except Exception as e:
            print(RED('UNABLE TO ADD USER: '+str(e)))
            log('UNABLE TO ADD USER: '+str(e))
            cx.close()
            return 0    
    
    def pkgAdd():
        while 1:#add package
            print(MENU("Create new package"))
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

            cnf=input(GREEN(f'CONFIRM THE PRVIDED DATA: \n    PACKAGE NAME: {name}\n  PACKAGE SPEED: {speed}\n    PACKAGE DAYS: {days}\n  MAX USERS: {users}\n    PRICE: {price}\n   PACKAGE: {p_type}\n\n>>>[Y/N] '))
                
            if cnf.strip().capitalize()=='Y':
                hermes.add_pkg(name,speed,days,users,price,p_type)
                return 1
            else:
                cnfb=input(RED(f'Create new package [Y/N]? '))
                if not cnfb.strip().capitalize()=='Y':
                    return 0
    def prgp(buf:str,count:int):#print <len> character strings
        #count=12
        l=len(buf)-count
        #print(l)

        while l<0:#word count has not yet reached 12 characters
            buf = buf + ' '
            if len(buf)-count ==0:
                break
            buf = ' '+ buf
            if count-len(buf) ==0:
                break
            
        while l>0:
            buf = buf[0:count]
            #bb=bb/2
            l=len(buf)-count
            break
        return buf +'|'   
    
    def accounts():
        cx = sqlite3.connect(database)
        cu = cx.cursor()
        cu.execute('Select * from account')
        dat=cu.fetchall()
        cu.close()
        print(f"+{'-'*12}+{'-'*12}+{'-'*12}+{'-'*12}+{'-'*12}+{'-'*12}+{'-'*12}+{'-'*12}+")
        print(f"|{hermes.prgp('acc',12)}{hermes.prgp('name',12)}{hermes.prgp('phone',12)}{hermes.prgp('package',12)}{hermes.prgp('username',12)}{hermes.prgp('password',12)}{hermes.prgp('installDdate',12)}{hermes.prgp('balance',12)}")
        print(f"+{'-'*12}+{'-'*12}+{'-'*12}+{'-'*12}+{'-'*12}+{'-'*12}+{'-'*12}+{'-'*12}+")

        for d in dat:

            print(f"|{hermes.prgp(str(d[0]),12)}{hermes.prgp(str(d[1]),12)}{hermes.prgp(str(d[2]),12)}{hermes.prgp(str(d[3]),12)}{hermes.prgp(str(d[4]),12)}{hermes.prgp(str(d[5]),12)}{hermes.prgp(str(d[6]),12)}{hermes.prgp(str(d[7]),12)}",flush=True)
        
        print(f"+{'-'*12}+{'-'*12}+{'-'*12}+{'-'*12}+{'-'*12}+{'-'*12}+{'-'*12}+{'-'*12}+")

    def status():
        try: 
            ls=[]
            usls=list(cache_sessions.keys())
            for c in usls:
                print(f'{cache_sessions[c]["start date"]}/{cache_sessions[c]["start time"]}')
                ls.append(f'{cache_account[c]["name"]}[{c}] {cache_sessions[c]["start date"]}/{cache_sessions[c]["start time"]} => {cache_sessions[c]["end date"]}/{cache_sessions[c]["end time"]}')
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
                users_ls.append(f"{cache_account[us]['name']} [{us}]")
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
            return 1
            
        except Exception as e:
            print(RED('UNABLE TO GET USER SESSION EDIT: '+str(e)))
            log('UNABLE TO GET USER SESSION EDIT: '+str(e))
            cx.close()
            return 0 
    
    def compensation():
        try:
            usrs=list(cache_account.keys())
            accomp=[]
            for x in usrs:
                accomp.append(f'{cache_account[x]["name"]} [{x}]')
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
            log(RED(f'ERROR RUNNING COMPENSATIONS: [{str(e)}]'))
            return 0

    def startup():#what to do when the program first runs
        try:
            print('\033c', end='')
            print(lg)
            print(GREEN(f'{tme()}HERMES WINGU SERVICE STARTUP \n '))
            log('HERMES WINGU SERVICE STARTUP PROCESS...') 

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
                    log(f'DATABASE FILE NOT FOUND AT {database}. Cannot proceed.')
                    sys.exit()

                if not cache() :
                    print("cache FAIL")
                    log("cache FAIL")

                cx = sqlite3.connect(database)
                cu = cx.cursor()
                cu.execute('Select * FROM account')
            
                
                print(GREEN(f'{tme()} {database} SQL SERVER AVAILABLE'))
                cx.close()
            except Exception as e:
                print(f'{tme()}ERROR. SQL SERVER UNREACHABLE')
                log('ERROR. SQL SERVER UNREACHABLE')
                sys.exit() #EXIT PROGRAM

            #2. RUN SESSION MONITOR TO DISCONNECT ANY UNAUTHORISED USERS
            print('Loading....')
            hermes.session_monitor()

            #3. MIKROTIK ACTIVE CHECKER

            otp=hermes.dbcommunication('select username,name,acc from account')
            cmd=[]
            for un in otp:
                cmd.append(f'ip hotspot user print detail where name="{un[0]}"')
            ssh_otp_list=hermes.ssh_command(cmd)
            c=0

            for ot in ssh_otp_list:
                try: 
                    if not 'limit-uptime' in ot: #find connected users
                        if not cache_sessions[otp[c][2]]["status"]== 'active':

                                print(f'{RED("User")} {MENU(otp[c][1])} {RED("is connected yet has no active session")}')
                                log(f'User {(otp[c][1])} is connected yet has no active session"')
                except Exception as e:
                    print(RED(f'ERROR CONFIRMING SESSION STATUS FOR {(otp[c][1])}'))
                    log(f'ERROR CONFIRMING SESSION STATUS FOR {otp[c][1]}')

                c=c+1
            print('\n\n')

            return 1
                    
        except Exception as e:
            print(RED(f'{tme()}FAIL RUNNING STARTUP. ERROR: {str(e)}'))
            log(f'FAIL RUNNING STARTUP. ERROR: {str(e)}')
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
            print(RED(f'{tme()}FAIL RUNNING MANUALLY. ERROR: {str(e)}'))
            log(f'{tme()}FAIL RUNNING MANUALLY. ERROR: {str(e)}')
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
                    print(MENU(f'   {cache_account[line[1]]["name"]} => {line[5]} / {line[6]}'))
                    SCHEDULED_SESSIION_DISSCONNECT.append(line[5]+'|'+line[6])        
                
            print('\n\n')

            if len(SCHEDULED_SESSIION_DISSCONNECT) >= 1:

                print(GREEN(f'{tme()} RUNNING AUTO SESSION MONITOR.SERVICE.'))
                log('RUNNING AUTO SESSION MONITOR.SERVICE.')
                # Convert each date string in the list to a datetime object
                date_objects = [datetime.strptime(date, '%d-%b-%Y|%I:%M %p') for date in SCHEDULED_SESSIION_DISSCONNECT]
                smallest_date = min(date_objects)
                dte_lst=str(smallest_date.strftime('%d-%b-%Y|%I:%M %p')).split('|')
                next_expiery = datetime.combine(datetime.strptime(dte_lst[0], "%d-%b-%Y").date(), datetime.strptime(dte_lst[1], "%I:%M %p").time())

                print(MENU(f"Next disconnection {next_expiery}"))
                log(f"Next disconnection {next_expiery}")
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


                   
def main():
    menu_list=['Users','Sessions','Payments','SWITCH TO AUTO_MONITOR','MANUAL CLI','Package','EXIT']
    a=str(menu(menu_list))
    if a=='1':#add user
        b=str(menu(['Accounts','Add user','Back']))
        if b=='3':
            main()
        elif b=='1':
            hermes.accounts()
        elif b=='2':
            print(GREEN('SWITCHING TO ADD USER'))
            hermes.add_user()
    elif a == '2':#session
        b=str(menu(['Active Sessions','Edit Session','Session Compensation','Back']))
        if b=='4':
            main()
        elif b=='1':
            print(GREEN('CURRENT SESSIONS'))
            hermes.status()
        elif b=='2':
            print(GREEN(f'RUNNING SESSION EDIT...'))
            hermes.session_edit()
        elif b=='3':
            print(GREEN(f'RUNNING COMPENSATION...'))
            hermes.compensation()

    elif a=='3':#payments
        b=str(menu(['Add payment','Payment History','Back']))
        if b=='3':
            main()
        elif b=='1':
            def_date_lst=time.ctime().strip().split(' ')
            def_date=f'{def_date_lst[-3]}-{def_date_lst[1]}-{def_date_lst[-1]}'
            print("RUNNING PAYMENT MANAGER SERVICE...\n\n")
            while 1:
                #SELECT SOURCE BY SELECTING ACCOUNT
                acc=[]
                acc_long=[]
                acc=list(cache_account.keys())
                pppoe_acc=[]
                pppoe_acc=list(cache_pppoe.keys())
                combined_acc=acc+pppoe_acc
                for ac in combined_acc:
                    if ac in acc:
                        acc_long.append(f'{cache_account[ac]["name"]} -> {ac}')
                    elif ac in pppoe_acc:
                        acc_long.append(f'{cache_pppoe[ac]["name"]} -> {ac}')

                acc_long.append('SELECT ACCOUNT BY PHONE NO')
                acc_long.append('EXIT')# add an exit setup

                selection = acc_long[menu(acc_long)-1]

                if selection=="EXIT":
                    print(GREEN('EXITING'))
                    return 0
                elif selection=="SELECT ACCOUNT BY PHONE NO":
                    cont=input('INPUT PHONE NO: ').strip()
                    if not cont in list(cache_contacts.keys()):
                        cnf=input(RED(f'THE CONTACT {cont} DOES NOT EXIST IN DATABASE.\nDo you want to add contact [Y/N]? '))
                        if cnf.strip().capitalize()=='Y':
                            print("SELECT USER ACCOUNT: ")
                            ld_list=[]
                            for ch in cache_account:
                                ld_list.append(f"{cache_account[ch]['name']} : {ch}")

                            for cp in cache_pppoe:
                                ld_list.append(f"{cache_pppoe[cp]['name']} : {cp}")

                            otp=menu(ld_list)-1
                            cnf = input(f'CONFIRM {ld_list[otp]} [Y/N] ')
                            if cnf.strip().capitalize() == 'Y':

                                print(GREEN('CONFIRMED..'))
                                acc=ld_list[otp].split(':')[1].strip()
                                if 'Wn' in acc:
                                    phone=cache_pppoe[ld_list[otp].split(':')[1].strip()]["phone"]
                                    acc_type='pppoe'
                                    selection=f'{cache_pppoe[acc]["name"]} [{acc}]'
                                elif 'Wp' in acc:
                                    phone=cache_account[ld_list[otp].split(':')[1].strip()]["phone"]
                                    acc_type='hotspot'
                                    selection=f'{cache_account[acc]["name"]} [{acc}]'


                                cx = sqlite3.connect(database)
                                cu = cx.cursor()
                                cu.execute(f'SELECT cid FROM contacts')
                                cid=str(int(cu.fetchall()[-1][0])+1)
                                cu.execute(f'INSERT INTO contacts VALUES({cid},"{acc}","{phone}")')
                                cx.commit()
                                cx.close()
                                print(f'contact added: [{cid},"{acc}","{phone}"]')


                                source_acc=acc
                                source_cont=phone
                            else:
                                print(RED('ERROR: CANNOT PROCEED WITH NO ACCOUNT PROVIDED'))
                                return 0

                        else:
                            print(RED('ERROR: CANNOT PROCEED WITH NO ACCOUNT PROVIDED'))
                            return 0

                    #if contact is found
                    else:
                        source_acc=cache_contacts[cont]['account']
                        source_cont=cont


                else:
                    source_acc=selection.split('-> ')[1].strip()
                    acl=[]
                    for key, value in cache_contacts.items():
                        if value.get("account") == source_acc:
                            acl.append(key)

                    if len(acl)==1:
                        source_cont=acl[0]
                    else:
                        source_cont=acl[menu(acl)-1]



                code=input('INPUT TRANSACTION CODE: ')
                ammount=input('INPUT AMOUNT: ')
                #source=input('INPUT SOURCE: ')
                date=input(f'INPUT DATE [{def_date}] : ')
                if date == '':
                    date= str(def_date)
                timet=input('INPUT TIME[hh:mm PM/AM]: ')
                conf=input(MENU(f'\nCODE: {code},\n  AMOUNT: {ammount},\n  Name: {selection}\n   SOURCE : {source_cont},\n   DATE : {date},\n    TIME: {timet}\n ')+' CONFIRM DATA Y/N: ')

                if conf.strip().capitalize()=='Y':
                    hermes.payments(code,ammount,source_cont,date,timet)
                    break
                else:
                    cn=input(MENU('DO YOU WANT TO EXIT [Y/N]?'))
                    if cn.strip().capitalize()=='Y':
                        break
        elif b=='2':
            print(GREEN('SWITCHING TO ADMIN SESSION CHECK'))
            _admin.accounting()

    elif a=='4':#back
        print(GREEN('SWITCHING BACK TO AUTO'))
        hermes.run()
    
    elif a=='5':#manual
        print(GREEN('SWITCHING TO MANUAL CLI'))
        hermes.manual()
    
    elif a=='6':#package
        b=str(menu(['Add Package','Back']))
        if b=='1':
            print(GREEN('Adding package'))
            hermes.pkgAdd()


    elif a=='7':#exit
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
if not input_fl in dir:
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
hermes.startup()

#infinite loop
while 1:
	hermes.run()
