from django.contrib import admin
from SupermarketManagement import models

# Register your models here.
admin.site.register(models.Customer)
admin.site.register(models.Staff)
admin.site.register(models.SalesReturn)
admin.site.register(models.Supplier)
admin.site.register(models.PurchaseReturn)
admin.site.register(models.ProcuredItems)
admin.site.register(models.OrderedItems)
admin.site.register(models.Membership)
admin.site.register(models.Order)
admin.site.register(models.Product)
admin.site.register(models.Invoice)
admin.site.register(models.Procurement)

