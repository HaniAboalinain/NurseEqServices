from django.db import models

# Create your models here.


class Equipment(models.Model):
    name = models.CharField(null=False, blank=False, max_length=255)
    quantity = models.IntegerField(null=False, blank=False)
    available = models.BooleanField()
    image = models.ImageField(upload_to='media/eq_pic', null=True, blank=True)
    description = models.TextField(null=False, blank=False)
    privacy_policy = models.BooleanField(null=False, blank=False)
    price = models.FloatField(null=False, blank=False)

    def __str__(self):
        return self.name
