from django.db import models
import uuid
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


# client model
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='client/profile_pic/', blank=True, null=True)
    phone_number = models.CharField(max_length=25, blank=True)
    stripe_client_id = models.CharField(max_length=225, blank=True)
    stripe_payment_id = models.CharField(max_length=225, blank=True)
    stripe_card_last_octet = models.CharField(max_length=225, blank=True)

    def __str__(self):
        return self.user.get_full_name()

# Courier model
# ---------------------------------------------------------------------------
class Courier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    C_Latitude = models.FloatField(default=0)
    C_Longitude = models.FloatField(default=0)
    paypal_mail = models.EmailField(max_length=225, blank=True)
    fcm_token = models.TextField(blank=True)
    
    def __str__(self):
        return self.user.get_full_name()
# ---------------------------------------------------------------------------
# category model
class category(models.Model):
    slug = models.CharField(max_length=225, unique=True)
    name = models.CharField(max_length=225)

    def __str__(self):
        return self.name
# Request model
# ---------------------------------------------------------------------------
class Request(models.Model):
    SMALL_SIZE = "Small"
    MEDIUM_SIZE = "Medium"
    LARGE_SIZE = "Large"
    SIZES = (
        (SMALL_SIZE, 'Small'),
        (MEDIUM_SIZE, 'Medium'),
        (LARGE_SIZE, 'Large'),
    )
    CREATING_STATUS = 'Creating'
    PROCESSING_STATUS = 'Processing'
    PICKING_STATUS = 'Picking'
    DELIVERING_STATUS = 'Delivering'
    COMPLETED_STATUS = 'Completed'
    CANCELED_STATUS = 'Canceled'
    STATUSES = (
        (CREATING_STATUS,'Creating'),
        (PROCESSING_STATUS,'Processing'),
        (PICKING_STATUS,'Picking'),
        (DELIVERING_STATUS,'Delivering'),
        (COMPLETED_STATUS,'Completed'),
        (CANCELED_STATUS,'Canceled'),
    )
# first-step
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False )
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=225)
    description = models.CharField(max_length=300)
    category = models.ForeignKey(category, on_delete=models.SET_NULL, null=True, blank=True)
    size = models.CharField(max_length=25, choices=SIZES, default=MEDIUM_SIZE)
    amount = models.IntegerField(default=1)
    picture = models.ImageField (upload_to='Request/pictures')
    status = models.CharField(max_length=25,choices=STATUSES, default=CREATING_STATUS)
    created_at = models.DateField(default=timezone.now)
#second-step
    pickup_address  =models.CharField(max_length=225, blank=True)
    pickup_lat  =models.FloatField(default=0)
    pickup_lng  =models.FloatField(default=0)
    pickup_phone  =models.CharField(max_length=45, blank=True)
    pickup_name  =models.CharField(max_length=45, blank=True)
#third step 
    delivery_address  =models.CharField(max_length=225, blank=True)
    delivery_lat  =models.FloatField(default=0)
    delivery_lng  =models.FloatField(default=0)
    delivery_phone  =models.CharField(max_length=45, blank=True)
    delivery_name  =models.CharField(max_length=45, blank=True)
#forth step 
    duration = models.IntegerField(default=0)
    distance = models.FloatField(default=0)
    price = models.FloatField(default=0)
#delivery prove
    pickup_picture = models.ImageField(upload_to='tasks/pickup_pic/',null=True, blank=True)
    pickup_Time = models.DateField(null=True, blank=True)

    delivery_picture = models.ImageField(upload_to='tasks/delivery_pic/',null=True, blank=True)
    delivered_Time = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f" Item :{self.name} in {self.category}"


class Transaction(models.Model):
    EARNED__STATUS = "earned"
    REFUND_STATUS = "refund"
    STATUSES = (
        (EARNED__STATUS,'earned'),
        (REFUND_STATUS,'refund'),
    )
    stripe_request_payment_id = models.CharField(max_length=255, unique=True)
    task_request = models.ForeignKey(Request, on_delete=models.CASCADE )
    payment_amount = models.FloatField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=25, choices=STATUSES, default=EARNED__STATUS)


    def __str__(self):
        return self.stripe_request_payment_id
    