from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from equipment.models import Equipment
from user.models import CustomUser

# Create your models here.
CITIES = (('', _('--- Choose city ---')),
          ('amman', 'Amman'), ('irbid', 'Irbid'), ('zarqa', 'Al-Zarqa'),
          ('aqapa', 'Al-Aqapa'), ('maan', 'Maan'), ('mafraq', 'Al-Mafraq'),
          ('karak', 'Al-Karak'), ('tafilah', 'Al-Tafilah'), ('madaba', 'Madaba'),
          ('jarash', 'Jarash'),)

DELIVERY_WAY = (('', _('--- Choose Delivery Way ---')),
                ('delivery', 'Delivery'), ('receive', 'Receive'),)

PAYMENT_METHOD = (('cash', 'Cash'), ('visa', 'Visa'),)


class EquipmentReservation(models.Model):
    eq_name = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name='equipment',
                                related_name='eq_name')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='User',
                             related_name='user')
    eq_count = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Equipment Count"),
                                           validators=[MaxValueValidator(5), MinValueValidator(1)])
    duration_from = models.DateField()
    duration_to = models.DateField()
    price = models.FloatField()
    id_photo = models.ImageField(upload_to='media/id_photos', null=True, blank=True)
    privacy_policy = models.BooleanField(null=False, blank=False)
    delivery_way = models.CharField(choices=DELIVERY_WAY, max_length=255)
    city = models.CharField(choices=CITIES, max_length=255)
    address = models.CharField(null=False, blank=False, max_length=500)
    payment_method = models.CharField(choices=PAYMENT_METHOD, max_length=255)
    card_number = models.CharField(max_length=14, blank=True, null=True, validators=[RegexValidator(r'^[0-9]{14}$')])
    visa_exp_date = models.DateField(blank=True, null=True)
    cvv = models.CharField(max_length=3, blank=True, null=True, validators=[RegexValidator(r'^[0-9]{3}$')])

    def __str__(self):
        return f'{self.eq_name.name} -------- Reservation made by: {self.user.username}'

    # def get_price(self):
    #     total_price = self.eq_name.price * self.eq_count
    #     return total_price
