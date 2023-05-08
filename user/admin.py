from django.contrib import admin

# Register your models here.
from user.models import CustomUser, Staff, NurseRequest

admin.site.register(CustomUser)
admin.site.register(Staff)
admin.site.register(NurseRequest)
