from django.contrib import admin
from . import models

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['client','courier','courier_Paypal','stripe_request_payment_id','task_request','payment_amount','status','created_at']
    list_filter = ['status',]

# client info 
    def client (self, obj):
        return obj.task_request.client
# courier info 
    def courier (self, obj):
        return obj.task_request.courier
# courier pAYPAL 
    def courier_Paypal (self, obj):
        return obj.task_request.courier.paypal_mail if obj.task_request.courier else None
# Register your models here.
admin.site.register(models.Client)
admin.site.register(models.Courier)
admin.site.register(models.category)
admin.site.register(models.Request)
admin.site.register(models.Transaction,TransactionAdmin)
