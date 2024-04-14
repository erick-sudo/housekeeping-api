from django.db import models
from django.conf import settings

# Create your models here.
class Cleaner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return f"Cleaner: {self.user.email}"
    
class CleanType(models.Model):
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self) -> str:
        return self.name
    
class SubService(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    clean_type = models.ForeignKey(CleanType, related_name='sub_services', on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.name
    
class CleaningFrequency(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
class PaymentMethod(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('CREDIT_CARD', 'Credit Card'),
        ('DEBIT_CARD', 'Debit Card'),
        ('PAYPAL', 'PayPal'),
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('OTHER', 'Other')
    ]

    name = models.CharField(max_length=100, choices=PAYMENT_METHOD_CHOICES)

    def __str__(self):
        return self.name
    
class CreditCard(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="credit_card", on_delete=models.CASCADE)
    cardholder_name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=16)
    expiration_date = models.CharField(max_length=4)
    cvv = models.CharField(max_length=4)
    
    def __str__(self):
        return f"{self.cardholder_name} - {self.card_number[-4:]}"
    
class AccessInfo(models.Model):
    address_name = models.CharField(max_length=255)
    address_code = models.CharField(max_length=50)
    how_to_get_in = models.TextField()
    any_pets = models.BooleanField(default=False)
    pets_description = models.CharField(max_length=255, blank=True, null=True)
    additional_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.address_name
    
class Booking(models.Model):
    
    BOOKING_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled')
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='bookings', on_delete=models.CASCADE)
    services = models.ManyToManyField(SubService, related_name='bookings', serialize=True)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    cleaning_frequency = models.ForeignKey(CleaningFrequency, on_delete=models.CASCADE)
    payment = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=20, choices=BOOKING_STATUS_CHOICES, default='PENDING')
    
    access_info = models.ForeignKey(AccessInfo, related_name="bookings", on_delete=models.CASCADE)
    
    cleaners = models.ManyToManyField(Cleaner, related_name="bookings")
    
    @property
    def cleaning_fee(self):
        return 456.56
    
    def __str__(self):
        return f"BookingID#{self.id} - Status#{self.get_status_display()} - StartDate#{self.start_date} - EndDate#{self.end_date}"