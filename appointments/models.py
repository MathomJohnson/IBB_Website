from django.db import models

# Create your models here.
class Appointment(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.name
    
class Meeting(models.Model):
    mentor = models.CharField(max_length=200)
    time = models.CharField(max_length=100)
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    cancelled = models.BooleanField(default=False)

    def __str__(self):
        return self.mentor+", "+self.time+", "+str(self.year)+", "+str(self.month)+", "+str(self.day)+", "+str(self.cancelled)
