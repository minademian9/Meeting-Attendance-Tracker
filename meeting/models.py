from django.db import models

# Create your models here.


class Attendee(models.Model):
    name = models.CharField(max_length=200)
    mobile = models.IntegerField(default=0, null=True, blank=True)
    email = models.CharField(max_length=200, blank=True)

    # pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.name + "," + str(self.id)

    # def export(self):
    #     queryset = self._meta.objects.all()
    #     # can use the below method also
    #     # queryset = self.__class__.objects.all()
    #     return queryset


class AttendanceRecord(models.Model):
    member = models.ForeignKey(Attendee, models.SET_NULL, null=True)
    record_date = models.DateTimeField('date published')

    def __str__(self):
        return self.member.name + " " + str(self.record_date)
