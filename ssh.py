import paramiko
import time

mk_ip=""
mk_username=""
mk_password=""

def RED(txt:str):
    return '\033[91m'+str(txt)+'\033[0m'
def GREEN(txt:str):
    return '\033[92m'+str(txt)+'\033[0m'
def MENU(txt:str):
    return '\033[36m'+str(txt)+'\033[0m'


def tme():
    tme=f"[{time.ctime().strip().split(' ')[0]}, {time.ctime().strip().split(' ')[1]}/{time.ctime().strip().split(' ')[2]}/{time.ctime().strip().split(' ')[-1]} {time.ctime().strip().split(' ')[-2]}] "
    return tme

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
        #log('ERROR CONNECTING TO SSH SERVER: AUTHENTICATION FAIL')
        return f"Authentication failed, please check your credentials: {ssh_err}"
    
    except paramiko.SSHException as ssh_err:
        print(RED(f"{tme()}Unable to establish SSH connection: {ssh_err}"))
        #log(f"ERROR: Unable to establish SSH connection: {ssh_err}")
        return f"Unable to establish SSH connection: {ssh_err}"
    
    except Exception as e:
        print(RED(f"{tme()}An error occurred: {e}"))
        #log(f"SSH ERROR OCCURED: {e}")
        return f"An error occurred: {e}"
    
print (ssh_command())