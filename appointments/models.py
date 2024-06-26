from django.db import models

# Create your models here.    
class Meeting(models.Model):
    id = models.AutoField(primary_key=True)
    mentor = models.CharField(max_length=200)
    time = models.TimeField()
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    cancelled = models.BooleanField(default=False)

    def __str__(self):
        return self.mentor+" at "+str(self.time)+" on "+str(self.month)+"/"+str(self.day)+"/"+str(self.year)+". Cancelled: "+str(self.cancelled)

class ScheduledMeeting(models.Model):
    user_id = models.IntegerField()
    datetime_scheduled = models.DateTimeField()

    def __str__(self):
        return "User #" + str(self.user_id) + " has a meeting scheduled"

class GoogleToken(models.Model):
    id = models.AutoField(primary_key=True)
    access_token = models.CharField(max_length=800)
    refresh_token = models.CharField(max_length=600)
    expiration = models.DateTimeField()

    def __str__(self):
        return "Token expires on " + str(self.expiration)