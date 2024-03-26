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
from datetime import datetime , timedelta
import time
import paramiko
import os
import sys
#import threading
#import msvcrt


from .models import Payment,Pkgs,Logs,pppoe,Contacts
from .models import Users,Sessions,Finances

#VARIABLES
mk_ip = '192.168.88.1'
mk_username = 'admin'
mk_password = 'admin'
hotspotServerName='hs-new_wingu'


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

class hermes:
    def ssh_command(cmds:list):
        # Establish SSH connection to the MikroTik router
        try:
            output=[]
            if len(cmds)<1:
                return 0,'SSH INPUT LIST < 1'
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=mk_ip, username=mk_username, password=mk_password,timeout=30)
            print(GREEN(f"{tme()}CONNECTED TO SERVER VIA SSH"))
            
            for cmd in cmds:
                print(f'Running command [{cmd}]')
                continue
                stdin, stdout, stderr = ssh_client.exec_command(f'log warning "auto running command {cmd}"')
                stdin, stdout, stderr = ssh_client.exec_command(cmd)
                output.append(stdout.read().decode('utf-8'))
            #print(MENU(output))
            ssh_client.close()
            return 1,output

        except paramiko.AuthenticationException:
            print(RED(f"{tme()}Authentication failed, please check your credentials."))
            return  0,f"Authentication failed, please check your credentials: {ssh_err}"
        
        except paramiko.SSHException as ssh_err:
            print(RED(f"{tme()}Unable to establish SSH connection: {ssh_err}"))
            return 0,f"Unable to establish SSH connection: {ssh_err}"
        
        except Exception as e:
            print(RED(f"{tme()}An error occurred: {e}"))
            return 0,f"An error occurred: {e}"

    def userSessionMonitor(sm_acc=None):

        try:
            #check if user has an active session. if so,leave.
            #else, get money from sm_acc and create a new session
            print("RUNNING SESSION MONITOR")

            if not sm_acc == None:#if a user is specified, check even they have an inactive session

                if not Sessions.objects.filter(acc=sm_acc,status='active').exists(): #if no active session create new session
                    ac=Users.objects.get(acc=sm_acc)
                    pkgDb=Pkgs.objects.get(pno=ac.package)
                    print(f'User {ac.name} has no active session.\n Creating session...')

                   
                    PKGU=ac.package
                    BALU=ac.balance
                    PKG_PRICEU=pkgDb.price#PRICE OF THE PACKAGE
                    PKG_NAMEU=pkgDb.name#NAME OF THE PACKAGE
                    days_to_addU=pkgDb.days#HOW MANY DAYS THE PACKAGE COVERS


                    if BALU >= PKG_PRICEU:#if balance is enough to parchase nxt package
                        #remove money from account
                        fin_sub=Finances(acc=ac.acc,moneyIn=0.00,moneyOut=PKG_PRICEU,description=f'{ac.acc} {PKG_NAME} SUBSCRIPTION RENEWAL',date=str(tme()))
                        fin_sub.save()

                        #update balance for removal
                        BALU=BALU-PKG_PRICEU
                        user_db_ac=Users.objects.get(acc=sm_acc)
                        user_db_ac.balance=BALU
                        user_db_ac.save()
                        print(f'{sm_acc} Balance updated to {BALU}')

                        #create next session
                        
                        TME=time.ctime().split(' ')
                        S_DATE=f'{TME[-3]}-{TME[1]}-{TME[-1]}'
                        S_TIME = datetime.strptime(TME[-2], "%H:%M:%S").strftime("%I:%M %p")
                        E_DATE = (datetime.strptime(S_DATE, "%d-%b-%Y") + timedelta(days=days_to_addU)).strftime("%d-%b-%Y")

                        ses_add=Sessions(acc= sm_acc,profile= PKG_NAMEU, startDate= S_DATE, startTime= S_TIME, endDate= E_DATE, endTime= S_TIME, status = "active",creation_date=str(tme()))
                        ses_add.save()
                        print(GREEN(f'{tme()}New LOCAL session is created for {ac.name} with the following values. (package : "{PKG_NAMEU}",start date : "{S_DATE}",start time : "{S_TIME}",end date : "{E_DATE}", end time : "{S_TIME}","active")'))

                        if Pkgs.pkg_type == 'pppoe':
                            print(MENU(f'CREATING NEW REMOTE PPPoE SESSION FOR {ac.name}'))
                            cmd=[f'ppp secret set "{ac.username}" disabled=no']
                            hermes.ssh_command(cmd)
                        elif Pkgs.pkg_type  == 'hotspot':
                            print(MENU(f'CREATING NEW REMOTE HOTSPOT SESSION FOR {ac.name}'))
                            cmd=[f'ip hotspot user set "{ac.username}" limit-uptime=0']
                            hermes.ssh_command(cmd)      

                    else:
                        print(RED(f'USER {ac.name} ACCOUNT BALANCE IS STILL INSUFFICIENT. NO SESSION CREATED')) 

                else:
                    print(GREEN(f'USER {sm_acc} ALREADY HAS AN ACTIVE SESSION.'))           


               
            
            active_sess = Sessions.objects.filter(status='active')
            print(f'Number of active sessions: {active_sess.count()}')
           
            for sessDat in active_sess:#loop through active session
                print(f"{tme()} CHECKING ACTIVE SESSION FOR {sessDat.acc}")

                #check if session is over
                combined_datetime = datetime.combine(datetime.strptime(sessDat.endDate, "%d-%b-%Y").date(), datetime.strptime(sessDat.endTime, "%I:%M %p").time())
                if combined_datetime <= datetime.now():
                    #(1) SET THE SESSION TO EXIRED
                
                    print(f"SESSION EXPIRED FOR [{sessDat.acc}]")
                    sessDat.status='expired'
                    sessDat.save()
                    
                    #(2)CHECK IF THE ACCOUNT HAS ENOUGH TO ACTIVATE THE NEXT SESSION
                    userObj=Users.objects.get(acc=sessDat.acc)
                    pkgObj=Pkgs.objects.get(pno=userObj.package)
                    
                    
                    BAL=userObj.balance
                    PKG_PRICE=pkgObj.price
                    PKG_NAME=pkgObj.name
                    days_to_add=pkgObj.days
                    uacc=userObj.acc

                    if BAL >= PKG_PRICE:#if balance is enough to parchase nxt package
                        #remove money from account
                        
                        removeFinance=Finances(acc=uacc,moneyIn=0.00,moneyOut=str(PKG_PRICE),description=f'{uacc} {PKG_NAME} SUBSCRIPTION RENEWAL',date=str(tme()))
                        removeFinance.save()

                        BAL=BAL-PKG_PRICE
                        userdo=Users.objects.get(acc=uacc)
                        userdo.balance=BAL
                        userdo.save()
                        
                        #create next session                        
                        TME=time.ctime().split(' ')
                        S_DATE=f'{TME[-3]}-{TME[1]}-{TME[-1]}'
                        S_TIME = datetime.strptime(TME[-2], "%H:%M:%S").strftime("%I:%M %p")
                        E_DATE = (datetime.strptime(S_DATE, "%d-%b-%Y") + timedelta(days=days_to_add)).strftime("%d-%b-%Y")
                        sess_add=Sessions(acc= uacc,profile= PKG_NAME, startDate= S_DATE, startTime= S_TIME, endDate= E_DATE, endTime= S_TIME, status = "active",creation_date=str(tme()))
                        sess_add.save()

                        print(GREEN(f'{tme()} NEW LOCAL SESSION CREATED FOR {uacc} [{userObj.acc}] WITH VALUES (package : "{PKG_NAME}",start date : "{S_DATE}",start time : "{S_TIME}",end date : "{E_DATE}",end time : "{S_TIME}","active","{str(tme())}")'))

                        #enable user on server
                        if pkgObj.pkg_type == 'pppoe':
                            print(MENU(f'CREATING NEW REMOTE PPPoE SESSION FOR {userObj.name}'))
                            cmd=[f'ppp secret set "{userObj.username}" disabled=no']
                            hermes.ssh_command(cmd)
                        elif pkgObj.pkg_type == 'hotspot':
                            print(MENU(f'CREATING NEW REMOTE HOTSPOT SESSION FOR {userObj.name}'))
                            cmd=[f'ip hotspot user set "{userObj.username}" limit-uptime=0']
                            hermes.ssh_command(cmd)
                   

                    else:
                        #disable user 
                        #disun=Users.objects.get(acc=uacc)
                        print(f'{tme()} USER {userObj.name} [{userObj.acc}] DISCONTINUED FROM CONNECTION')
                        #un=cache_account[acc_no]["username"]
                        if pkgObj.pkg_type== 'pppoe':
                            cmd=[f'ppp secret set "{userObj.username}" disabled=yes',f'ppp active remove [find name="{userObj.username}"]']
                            hermes.ssh_command(cmd)
                        elif pkgObj.pkg_type== 'hotspot':
                            cmd=[f'ip hotspot user set "{userObj.username}" limit-uptime=1s',f'ip hotspot active remove [find name="{userObj.username}"]']
                            hermes.ssh_command(cmd)
                            

            print('SESSION MONITOR COMPLETED')
            
        except Exception as e:
            print(RED(f'FAILED SESSION MONITOR: {str(e)}'))
            return 0,f'FAILED SESSION MONITOR: {str(e)}'

    def addUser(pkg_type:str,name:str,username:str,password:str,package:str):
        try:
            print(MENU('ADDING USER: '))
            cmd=[]            
            if pkg_type == 'hotspot':
                cmd.append(f'ip hotspot user add comment="{name}" name="{username}" password="{password}" profile="{package}"  server={hotspotServerName} limit-uptime=5m ')
                
            elif pkg_type == 'pppoe':
                cmd.append(f'ppp secret add comment="{name}" name="{username}" password="{password}" profile="{package}"  service=pppoe ')
                
            hermes.ssh_command(cmd)

            return 1
        except Exception as e:
            print(RED('UNABLE TO ADD USER: '+str(e)))
            return 0    
        
    def addPackage(name:str,speed:int,max_users:str,pkg_type:str):
        try:
            print(MENU('ADDING Package: '))
            cmd=[]            
            if pkg_type == 'hotspot':
                cmd.append(f'ip hotspot user profile add name="{name}" rate-limit="{speed}M/{speed}M" shared-users="{max_users}"')
                
            elif pkg_type == 'pppoe':
                cmd.append(f' ppp profile add name="{name}" rate-limit="{speed}M/{speed}M"')
                
            hermes.ssh_command(cmd)

            return 1
        except Exception as e:
            print(RED('UNABLE TO ADD USER: '+str(e)))
            return 0   

    def editPackage(name:str,speed:int,max_users:str,pkg_type:str):
        try:
            print(MENU('EDIT Package: '))
            cmd=[]            
            if pkg_type == 'hotspot':
                cmd.append(f'ip hotspot user profile edit name="{name}" rate-limit="{speed}M/{speed}M" shared-users="{max_users}"')
                
            elif pkg_type == 'pppoe':
                cmd.append(f' ppp profile set name="{name}" rate-limit="{speed}M/{speed}M"')
                
            hermes.ssh_command(cmd)

            return 1
        except Exception as e:
            print(RED('UNABLE TO ADD USER: '+str(e)))
            return 0 

    def userEdit(name:str,profile:str,username:str,password:str,pkg_type:str):
        try:
            print(MENU('EDIT USER: '))
            cmd=[]            
            if pkg_type == 'hotspot':
                cmd.append(f'ip hotspot user set {username} comment="{name}" name="{username}" password="{password}" profile="{profile}"  server={hotspotServerName}')
                
            elif pkg_type == 'pppoe':
                cmd.append(f'ppp secret set {username} comment="{name}" name="{username}" password="{password}" profile="{profile}"')
                
            hermes.ssh_command(cmd)

            return 1
        except Exception as e:
            print(RED('UNABLE TO EDIT USER: '+str(e)))
            return 0 

    