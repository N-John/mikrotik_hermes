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

class Active_sessions(models.Model):
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

