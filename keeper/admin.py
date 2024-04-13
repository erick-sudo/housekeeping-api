from django.contrib import admin
from .models import Cleaner, CleanType, SubService, CleaningFrequency, PaymentMethod, CreditCard, Booking

# Register your models here.
admin.site.register([Cleaner, CleanType, SubService, CleaningFrequency, PaymentMethod, CreditCard, Booking])