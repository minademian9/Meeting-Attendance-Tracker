from django.db import models

# Create your models here.


class Attendee(models.Model):
    name = models.CharField(max_length=200)
    mobile = models.IntegerField(default=0, null=True, blank=True)
    email = models.CharField(max_length=200, blank=True)

    # pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.name + "," + str(self.id)

    # def getdetails(self):
    #     return {"player_name": self.player_name,
    #     "player_choice": self.choice ,
    #     "bet_id" :self.bet.id
    #     , "bet_text":self.bet.bet_text
    #     , 'bet_solution' : self.bet.solution,
    #     'bet_value': self.value,
    #     'bet_owner':self.bet.owner}


class AttendanceRecord(models.Model):
    member = models.ForeignKey(Attendee, models.SET_NULL, null=True)
    record_date = models.DateTimeField('date published')

    # bet = models.ForeignKey(Attendee)  # on_delete=models.CASCADE

    def __str__(self):
        return str(self.id)
