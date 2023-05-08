from datetime import date

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

from django.utils.translation import ugettext_lazy as _

NURSE_TYPE = (
    ('PENDING', _('Pending')), ('REVIEW', _('Review')),
    ('APPROVED', _('Approved')), ('REJECTED', _('Rejected')),
)

CITIES = (('', _('--- Choose a City ---')),
          ('AMMAN', _('AMMAN')), ('ZARQA', _('ZARQA')), ('KARAK', _('KARAK')), ('MAFRAQ', _('MAFRAQ')),
          ('AQABA', _('AQABA')), ('IRBID', _('IRBID')),
          )


class CustomUser(AbstractUser):
    phone = models.CharField(unique=True, max_length=10, null=True, blank=True, verbose_name=_('Phone'))
    birth_date = models.DateField(null=True, default=timezone.now, verbose_name=_('Birth Date'))
    insurance = models.BooleanField(default=False, verbose_name=_('Do you have health insurance'))
    agreement = models.BooleanField(default=False, verbose_name=_('Terms & conditions'))
    session_number = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.get_full_name()

    def clac_age(self):
        today = date.today()
        age = today.year - self.birth_date.year
        return age


class NurseRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='UserRequest',
                             blank=True, null=True)
    state = models.CharField(max_length=255, choices=NURSE_TYPE, null=True, blank=True, default='PENDING')
    bio = models.TextField(null=True)
    major = models.CharField(max_length=255, null=True)
    certificate = models.ImageField(upload_to='media/certifications', null=True)
    exp_year = models.IntegerField(null=True)
    photo = models.ImageField(upload_to='media/doctor_photo', null=True)
    city = models.CharField(max_length=255, choices=CITIES, null=True)

    def save(self, *args, **kwargs):
        if self.pk:
            original_state = NurseRequest.objects.get(pk=self.pk).state
            if original_state != 'APPROVED' and self.state == 'APPROVED':
                staff = Staff.objects.create(user=self.user, bio=self.bio, major=self.major, city=self.city,
                                             certificate=self.certificate, exp_year=self.exp_year, photo=self.photo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.get_full_name()


class Staff(models.Model):  # Nurse model
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='User',
                             related_name='staff', blank=True, null=True)
    bio = models.TextField(null=True, blank=True)
    major = models.CharField(max_length=255, null=True, blank=True)
    certificate = models.ImageField(upload_to='media/certifications', null=True, blank=True)
    photo = models.ImageField(upload_to='media/doctor_photo', null=True, blank=True)
    exp_year = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=255, choices=CITIES, null=True)
    # rate = models.PositiveIntegerField(null=True, blank=True, default=5,
    #                                    validators=[MaxValueValidator(5), MinValueValidator(1)])

    def __str__(self):
        return self.user.get_full_name()


class Rate(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='User',
                             blank=True, null=True)
    doctor = models.ForeignKey(Staff, on_delete=models.CASCADE, verbose_name='Doctor',
                               blank=True, null=True)
    rate = models.PositiveIntegerField(null=True, blank=True, default=5,
                                       validators=[MaxValueValidator(5), MinValueValidator(1)])

    def __str__(self):
        self.doctor + ' ' + str(self.rate)
