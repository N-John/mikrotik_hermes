from django.db import models

class apiData(models.Model):
    tokens = models.TextField(primary_key=True)
    owner = models.TextField()
    username = models.TextField()
    password = models.IntegerField()
    creationDate = models.TextField()
    apiClass = models.TextField(db_column='class')
    status = models.TextField()

    class Meta:
        db_table = 'api'
        #managed = False

class api_sms(models.Model):
    sid = models.AutoField(primary_key=True)
    source = models.TextField()
    date = models.TextField()
    time = models.TextField()
    message = models.TextField()
    read = models.TextField()

    class Meta:
        db_table = 'api_sms'
        #managed = False
