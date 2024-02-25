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

#VARIABLES
input_fl='variables.txt'
log_file_name='service_log.txt'
running = True
account_nme={}

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

_hermes_service SERVICE IS CREATED BY JOHN TO MANAGE MIKROTIK ISP SERVICES VIA HOTSPOT AND PPPoE.
To run this code, make sure you can connect to the router/server and to the sql server.
Make sure the "variables.txt" file has the appropriate data 

DISCLAIMER:
BEFORE RUNNING, MAKE SURE YOU HAVE THE FOLLOWING
    sqlite3     -> used for sql database
    paramiko    -> used for ssh communication
    time        -> 
    datetime    ->

OWNER: JOHN NJOROGE
GITHUB: https://github.com/N-John/mikrotik__hermes_service.git \n\n
LAST MODIFIED: 6-Feb-2024
    '''

def tme():
    tt=time.ctime().strip().split(' ')
    tme=f"[{tt[3]}-{tt[1]}-{tt[-1]} {tt[-2]}] "
    return tme

def log(dat:str):
    with open (service_log_file,'a') as log:
        log.write(f'\n {tme()} {dat}')
    #print(f'{tme()} {dat}') #comment this line to reduce verbose

def _cache_update():
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
        cu.execute('SELECT * FROM pppoe_account')
        OUTPT=cu.fetchall()
        for data in OUTPT:
            cache_pppoe[data[0]]={"name"      :data[1],
                                "phone"       :data[2],
                                "location"    :data[3],
                                "ip"    :data[4],
                                "username"      :data[5],
                                "password"      :data[6],
                                "package"        :data[8],
                                "creation date" :data[7],
                                "balance"        :data[9]
                                }
        
        print(f"{'#'*10}] 100%\033[0m")
        cx.close()

        return 1
    except Exception as e:
        print('#'*10)
        print(f'USER CACHE FAIL: {str(e)}')
        return 1

class _hermes_service:
    def database_cmd(comm:str):
        try:
            print(f'Running db communication command [{comm}]')
            log(f'Running db communication command [{comm}]')
            cx = sqlite3.connect(database)
            cu = cx.cursor()
            cu.execute(comm)
            OUTPT=cu.fetchall()
            cx.commit()
            cx.close()
            #print(OUTPT)
            return OUTPT

        except Exception as e:
            print((f'FAILED SQL: {str(e)}'))
            log(f'FAILED SQL: {str(e)}')
            return 0
        
    def ssh_command(cmds:list):
        # Establish SSH connection to the MikroTik router
        try:
            output=[]
            if len(cmds)<1:
                return 0
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=mk_ip, username=mk_username, password=mk_password)
            print(f"{tme()}CONNECTED TO SERVER VIA SSH")
            log(f"{tme()}CONNECTED TO SERVER VIA SSH TO RUN COMMANDS {cmds}")
            
            for cmd in cmds:

                print(f'Running command [{cmd}]')
                stdin, stdout, stderr = ssh_client.exec_command(f'log warning "auto running command {cmd}"')
                stdin, stdout, stderr = ssh_client.exec_command(cmd)
                output.append(stdout.read().decode('utf-8'))
            #print(MENU(output))
            ssh_client.close()
            return output

        except paramiko.AuthenticationException:
            print(f"{tme()}Authentication failed, please check your credentials.")
            log('ERROR CONNECTING TO SSH SERVER: AUTHENTICATION FAIL')
            return f"Authentication failed, please check your credentials: {ssh_err}"
        
        except paramiko.SSHException as ssh_err:
            print(f"{tme()}Unable to establish SSH connection: {ssh_err}")
            log(f"ERROR: Unable to establish SSH connection: {ssh_err}")
            return f"Unable to establish SSH connection: {ssh_err}"
        
        except Exception as e:
            print(f"{tme()}An error occurred: {e}")
            log(f"SSH ERROR OCCURED: {e}")
            return f"An error occurred: {e}"

    def session_monitor():
        try:
            print("RUNNING SESSION MONITOR")
            log(f'RUNNING SESSION MONITOR')
            cx = sqlite3.connect(database)
            cu = cx.cursor()
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
                    log(f"SESSION EXPIRED FOR {account_nme[acc_no]}[{acc_no}].")
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
                        log(f'CREATING NEW SESSION FOR {account_nme[acc_no]}[{acc_no}].')
                        
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
                        sid=str(int(cu.fetchone()[0]) + 1)
                        cu.execute(f'INSERT INTO sessions VALUES({sid},"{acc_no}","{PKG_NAME}","{S_DATE}","{S_TIME}","{E_DATE}","{S_TIME}","active","{str(tme())}")')
                        print(f'{tme()} NEW LOCAL SESSION CREATED FOR {account_nme[acc_no]} WITH VALUES ({sid},package : "{PKG_NAME}",start date : "{S_DATE}",start time : "{S_TIME}",end date : "{E_DATE}",end time : "{S_TIME}","active","{str(tme())}")')

                        #enable user on server
                        cu.execute(f'SELECT username FROM account where acc = "{acc_no}"')
                        un=cu.fetchall()[0][0]

                        if cache_package[cache_account[acc_no]["package"]]["type"] == 'pppoe':
                            print((f'CREATING NEW REMOTE PPPoE SESSION FOR {account_nme[acc_no]}'))
                            cmd=[f'ppp secret set "{cache_account[acc_no]["username"]}" disabled=no']
                            _hermes_service.ssh_command(cmd)
                            log((f'CREATED NEW REMOTE PPPoE SESSION FOR {account_nme[acc_no]}'))

                        elif cache_package[cache_account[acc_no]["package"]]["type"] == 'hotspot':
                            print((f'CREATING NEW REMOTE HOTSPOT SESSION FOR {account_nme[acc_no]}'))
                            cmd=[f'ip hotspot user set "{cache_account[acc_no]["username"]}" limit-uptime=0']
                            _hermes_service.ssh_command(cmd)
                            log((f'CREATED NEW REMOTE HOTSPOT SESSION FOR {account_nme[acc_no]}'))
                   

                    else:
                        #disable user session
                        print(f'{tme()} USER {account_nme[acc_no]} DISCONTINUED FROM CONNECTION')
                        un=cache_account[acc_no]["username"]
                        if cache_package[cache_account[acc_no]["package"]]["type"] == 'pppoe':
                            cmd=[f'ppp secret set "{un}" disabled=yes',f'ppp active remove [find name="{un}"]']
                            _hermes_service.ssh_command(cmd)
                        elif cache_package[cache_account[acc_no]["package"]]["type"] == 'hotspot':
                            cmd=[f'ip hotspot user set "{un}" limit-uptime=1s',f'ip hotspot active remove [find name="{un}"]']
                            _hermes_service.ssh_command(cmd)
                        log(f'{tme()} USER {account_nme[acc_no]} DISCONTINUED FROM CONNECTION')
                            

            cx.commit()
            cx.close()
            print('SESSION MONITOR COMPLETED')

            return 1
            
        except Exception as e:
            cx.close()
            print((f'FAILED SESSION MONITOR: {str(e)}'))
            log(f'FAILED SESSION MONITOR: {str(e)}')
            return 0
    
    def startup():#what to do when the program first runs
        try:
            #print('\033c', end='')
            #print(lg)
            print((f'{tme()}_hermes_service WINGU SERVICE STARTUP \n '))
            log('_hermes_service WINGU SERVICE STARTUP PROCESS...') 

            #1.check if sql and log file exist is available
            try:
                if _cache_update() == 0:
                    print("cache failed.Exiting")
                    log("cache failed. Exiting")
                    sys.exit()

                cx = sqlite3.connect(database)
                cu = cx.cursor()
                cu.execute('Select * FROM account')
                dt=cu.fetchall()
                for l in dt:
                    accnt=l[0]
                    nme=l[1]
                    account_nme[accnt]=nme
                print((f'{tme()} {database} SQL SERVER AVAILABLE'))
                cx.close()
            except Exception as e:
                print(f'{tme()}ERROR. SQL SERVER UNREACHABLE')
                log('ERROR. SQL SERVER UNREACHABLE')
                sys.exit() #EXIT PROGRAM

            #2. RUN SESSION MONITOR TO DISCONNECT ANY UNAUTHORISED USERS
            print('Loading....')
            _hermes_service.session_monitor()

            #3. MIKROTIK ACTIVE CHECKER

            otp=_hermes_service.database_cmd('select username,name,acc from account')
            cmd=[]
            for un in otp:
                cmd.append(f'ip hotspot user print detail where name="{un[0]}"')
            ssh_otp_list=_hermes_service.ssh_command(cmd)
            c=0

            for ot in ssh_otp_list:
                try: 
                    if not 'limit-uptime' in ot: #find connected users
                        if not cache_sessions[otp[c][2]]["status"]== 'active':

                                print(f'{("User")} {(otp[c][1])} {("is connected yet has no active session")}')
                                log(f'User {(otp[c][1])} is connected yet has no active session"')
                except Exception as e:
                    print((f'ERROR CONFIRMING SESSION STATUS FOR {(otp[c][1])}'))
                    log(f'ERROR CONFIRMING SESSION STATUS FOR {otp[c][1]}')

                c=c+1

            return 1
                    
        except Exception as e:
            print((f'{tme()}FAILED RUNNING STARTUP. ERROR: {str(e)}'))
            log(f'FAILED RUNNING STARTUP. ERROR: {str(e)}')
            return 0
    
    def run():
        try:
            _cache_update()
            SCHEDULED_SESSIION_DISSCONNECT=[]
            cx = sqlite3.connect(database)
            cu = cx.cursor() 
            cu.execute('SELECT * FROM sessions WHERE status = "active"')
            OUTPT=cu.fetchall()
            cx.close()
            
            if not len(OUTPT) == 0:
                print("\n"+tme()+'ACTIVE SESSIONS: ')
                for line in OUTPT:
                    print((f'   {account_nme[line[1]]} => {line[5]} / {line[6]}'))
                    SCHEDULED_SESSIION_DISSCONNECT.append(line[5]+'|'+line[6])        
                
            print('\n\n')

            if len(SCHEDULED_SESSIION_DISSCONNECT) >= 1:

                print((f'{tme()} RUNNING AUTO SESSION MONITOR.SERVICE.'))
                log('RUNNING AUTO SESSION MONITOR.SERVICE.')
                # Convert each date string in the list to a datetime object
                date_objects = [datetime.strptime(date, '%d-%b-%Y|%I:%M %p') for date in SCHEDULED_SESSIION_DISSCONNECT]
                smallest_date = min(date_objects)
                dte_lst=str(smallest_date.strftime('%d-%b-%Y|%I:%M %p')).split('|')
                next_expiery = datetime.combine(datetime.strptime(dte_lst[0], "%d-%b-%Y").date(), datetime.strptime(dte_lst[1], "%I:%M %p").time())

                print((f"Next disconnection {next_expiery}"))
                log(f"Next disconnection {next_expiery}")
                while 1:
                    time.sleep(3)
                    if datetime.now()>= next_expiery:#IF NEXT EXPIERY HAS REACHED
                        print((f'{tme()} Internal system interupt. Exiting monitor.service to check active sessions...'))
                        log('Internal system interupt. Exiting monitor.service to check active sessions...')
                        _hermes_service.session_monitor()
                        return 1
            
            else:
                print((f'{tme()}NO SCHEDULED DISCONNECTION. EXITING.....'))
                log(f'NO SCHEDULED DISCONNECTION. EXITING.....')
                
            return 1

        except Exception as e:
            log('ERROR RUNNING _hermes_service: '+str(e))
            print(('ERROR RUNNING _hermes_service: '+str(e)))
            return 0


#################################################################

current_directory = os.getcwd()  # Get the current working directory
dir=os.listdir(current_directory)

service_log_file=os.path.join(current_directory, log_file_name)

if not os.path.exists(service_log_file):
    print((f'LOG FILE DOES NOT EXIST AT {service_log_file}'))
    with open(service_log_file,'w') as file:
        file.write(f'LOG FILE CREATED ON {tme()}')
    print((f'LOG FILE SUCCESSFULY CREATED AT {current_directory}'))


if not os.path.exists(os.path.join(current_directory, input_fl)):
    print(('INPUT FILE NOT FOUND'))
    print(f'Input file could not be found..EXITING PROGRAM')
    log(f'Input file could not be found..EXITING PROGRAM')
    sys.exit()


#VARIABLES FETCH
with open (os.path.join(current_directory, input_fl),'r') as infl:
    ld=infl.readlines()

database_name=ld[2].split('|')[2].strip()
#log_file_name=ld[4].split('|')[2].strip()
mk_ip = ld[6].split('|')[2].strip()
mk_username = ld[8].split('|')[2].strip()
mk_password = ld[10].split('|')[2].strip()
database = os.path.join(current_directory, database_name) 
#log_file= os.path.join(current_directory, log_file_name)


_hermes_service.startup()

#infinite loop
while 1:
	_hermes_service.run()
