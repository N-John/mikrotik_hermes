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
        managed = False

class Sessions(models.Model):
    sid           = models.AutoField(primary_key=True)  
    acc           = models.TextField() 
    profile       = models.TextField() 
    startDate   = models.TextField(db_column='start date') 
    startTime    = models.TextField(db_column='start time') 
    endDate   = models.TextField(db_column='end date')
    endTime   = models.TextField(db_column='end time') 
    status        = models.TextField() 
    #creation_date = models.TextField() 
    
    class Meta:
        db_table = 'sessions'
        managed = False


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
        db_table = 'account'
        managed = False

class Finances(models.Model):

    fid           = models.AutoField(primary_key=True)  
    acc           = models.TextField() 
    moneyIn       = models.IntegerField(db_column='money in') 
    moneyOut   = models.IntegerField(db_column='money out') 
    description    = models.TextField() 
    date   = models.TextField()
    
    class Meta:
        db_table = 'finances'
        managed = False

class Pkgs(models.Model):
    pno       = models.IntegerField(primary_key=True)      
    name      = models.TextField()     
    speed     = models.IntegerField()     
    days      = models.IntegerField()  
    max_users = models.IntegerField()     
    price     = models.DecimalField(max_digits=8,decimal_places=2)    
    pkg_type  = models.TextField(db_column='type')    

    class Meta:
        db_table = 'package' 
        managed = False

class Logs(models.Model):
    lid           = models.AutoField(primary_key=True) 
    topic       = models.TextField()
    date           = models.TextField()  
    time   = models.TextField() 
    desc    = models.TextField() 
    
    class Meta:
        db_table = 'logs'
        managed = False
