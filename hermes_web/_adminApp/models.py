from django.db import models

class Payment(models.Model):
    pid = models.AutoField(primary_key=True)
    acc = models.TextField()
    code = models.TextField()
    amount = models.IntegerField()
    source = models.TextField()
    date = models.TextField()
    time = models.TextField()

    class Meta:
        db_table = 'payments'
        #managed = False

class Sessions(models.Model):
    sid           = models.AutoField(primary_key=True)  
    acc           = models.TextField() 
    profile       = models.TextField() 
    startDate   = models.TextField(db_column='start date') 
    startTime    = models.TextField(db_column='start time') 
    endDate   = models.TextField(db_column='end date')
    endTime   = models.TextField(db_column='end time') 
    status        = models.TextField() 
    creation_date = models.TextField(db_column='creation date') 
    
    class Meta:
        db_table = 'sessions'
        #managed = False

class Users(models.Model):
    acc           = models.TextField(primary_key=True) 
    name       = models.TextField()
    phone       = models.TextField()
    package       = models.IntegerField()
    username       = models.TextField()
    password       = models.TextField() 
    install_date   = models.TextField() 
    balance       = models.DecimalField(max_digits=10,decimal_places=2)
    
    class Meta:
        db_table = 'hotspotAccounts'
        #managed = False

class Contacts(models.Model):
    cid           = models.IntegerField(primary_key=True) 
    account       = models.TextField()
    contact       = models.TextField()
    
    class Meta:
        db_table = 'contacts'
        #managed = False

class Finances(models.Model):

    fid           = models.AutoField(primary_key=True)  
    acc           = models.TextField() 
    moneyIn       = models.IntegerField(db_column='money in') 
    moneyOut   = models.IntegerField(db_column='money out') 
    description    = models.TextField() 
    date   = models.TextField()
    
    class Meta:
        db_table = 'finance'
        #managed = False

class Pkgs(models.Model):
    pno       = models.AutoField(primary_key=True)      
    name      = models.TextField()     
    speed     = models.IntegerField()     
    days      = models.IntegerField()  
    max_users = models.IntegerField()     
    price     = models.DecimalField(max_digits=8,decimal_places=2)    
    pkg_type  = models.TextField(db_column='type')    

    class Meta:
        db_table = 'packages' 
        #managed = False

class Logs(models.Model):
    lid    = models.AutoField(primary_key=True) 
    topic  = models.TextField()
    date   = models.TextField()  
    time   = models.TextField() 
    desc   = models.TextField() 
    
    class Meta:
        db_table = 'logs'
        #managed = False

class Notifications(models.Model):
    id           = models.AutoField(primary_key=True) 
    topic       = models.TextField()
    category       = models.TextField()
    to       = models.TextField()
    dateTime           = models.TextField()  
    notification    = models.TextField() 
    read    = models.BooleanField()

    class Meta:
        db_table = 'notifications'
        #managed = False\

class Messages(models.Model):
    id           = models.AutoField(primary_key=True) 
    sender=models.TextField()
    to       = models.TextField()
    dateTime           = models.TextField()  
    message    = models.TextField()
    read    = models.BooleanField()
    
    class Meta:
        db_table = 'messages'
        #managed = False

class pppoe(models.Model):
    acc     =models.TextField(primary_key=True)
    phone   =models.TextField()
    location=models.TextField()
    ip      =models.TextField()
    username=models.TextField()
    password=models.TextField()
    install_date=models.TextField(db_column='install date')
    name    =models.TextField()
    package =models.IntegerField()
    balance =models.IntegerField()


    class Meta:
        db_table = 'pppoeAccounts'
       # managed = False
        