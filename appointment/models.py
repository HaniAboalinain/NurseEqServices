import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from user.models import CustomUser, Staff, CITIES

WORKING_HOURS = (('', _('--- Choose Session time ---')),
                 ('8-9', '08:00 AM - 09:00 AM'), ('9-10', '09:00 AM - 10:00 AM'), ('10-11', '10:00 AM - 11:00 AM'),
                 ('11-12', '11:00 AM - 12:00 PM'), ('12-1', '12:00 PM - 01:00 PM'), ('1-2', '01:00 PM - 02:00 PM'),
                 ('2-3', '02:00 PM - 03:00 PM'), ('3-4', '03:00 PM - 04:00 PM'), ('4-5', '04:00 PM - 05:00 PM'),
                 ('5-6', '05:00 PM - 06:00 PM'),)

APPOINTMENT_STATUS = (('AVAILABLE', _('Available')), ('BOOKED', _('Booked')),
                      ('APPROVED', _('Approved')), ('UNAVAILABLE', _('Unavailable')),
                      ('DONE', _('Done')),
                      )

MAJOR = (('', _('--- Choose Major ---')), ('Pediatric', _('Pediatric nursing')), ('Elderly', _('Elderly nursing')),
         ('Kidney', _('Kidney disease')), ('Other', _('Other')),
         )

APPOINTMENT_TYPE = (('EMERGENCY', _('Emergency')), ('NORMAL', _('Normal')),)


class Appointment(models.Model):
    date = models.DateField()
    major = models.CharField(max_length=255, choices=MAJOR, null=True)
    session_time = models.CharField(max_length=255, choices=WORKING_HOURS, null=True)
    message = models.TextField(null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    doctor = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=255, choices=APPOINTMENT_STATUS, null=True, default='AVAILABLE')
    type = models.CharField(max_length=255, choices=APPOINTMENT_TYPE, null=True, default='NORMAL')
    city = models.CharField(max_length=255, choices=CITIES, null=True,)

    def __str__(self):
        return f'{self.message} --------- appointment made by: {self.user}'
