from django.db import models

# Create your models here.


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.BigIntegerField()
    product_name = models.CharField(max_length=20)
    brand = models.CharField(max_length=15)
    price = models.IntegerField()
    available_stock = models.IntegerField()
    quantity_sold = models.IntegerField()
    discounted_price = models.IntegerField()

    def __str__(self):
        return str(self.product_name)


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    customer_ph_no = models.BigIntegerField()
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    addr_line_1 = models.CharField(max_length=25)
    addr_line_2 = models.CharField(max_length=25)

    def __str__(self):
        return str(self.first_name + ' ' + self.last_name)


class Membership(models.Model):
    id = models.AutoField(primary_key=True)
    customer_ph_no = models.BigIntegerField()
    order_id = models.IntegerField()
    pts_added_or_redeemed = models.IntegerField()

    def __str__(self):
        return str(self.customer_ph_no)


class Invoice(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.IntegerField()
    amount_paid = models.IntegerField()
    change_generated = models.IntegerField()

    def __str__(self):
        return str(self.order_id)


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.IntegerField()
    order_date = models.DateField()
    customer_ph_no = models.BigIntegerField()
    mode_of_payment = models.CharField(max_length=10)
    staff_id = models.IntegerField()

    def __str__(self):
        return str(self.order_id)


class SalesReturn(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.IntegerField()
    product_id = models.IntegerField()
    quantity = models.IntegerField()
    amount_to_pay = models.IntegerField()
    replacement_order_id = models.IntegerField()

    def __str__(self):
        return str(self.order_id)


class OrderedItems(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.IntegerField()
    product_id = models.IntegerField()
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.order_id)


class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    supplier_ph_no = models.BigIntegerField()
    agency_name = models.CharField(max_length=20)
    addr_line_1 = models.CharField(max_length=25)
    addr_line_2 = models.CharField(max_length=25)

    def __str__(self):
        return str(self.agency_name + ' ' + '-' + str(self.supplier_ph_no))


class Procurement(models.Model):
    id = models.AutoField(primary_key=True)
    batch_no = models.IntegerField()
    bill_no = models.CharField(max_length=10)
    supplier_ph_no = models.BigIntegerField()
    amount_to_pay = models.IntegerField()
    delivery_date = models.DateField()

    def __str__(self):
        return str(self.batch_no)


class PurchaseReturn(models.Model):
    id = models.AutoField(primary_key=True)
    batch_no = models.IntegerField()
    date = models.DateField()
    amount_returned = models.IntegerField()
    product_id = models.IntegerField()

    def __str__(self):
        return str(self.batch_no)


class ProcuredItems(models.Model):
    id = models.AutoField(primary_key=True)
    batch_no = models.IntegerField()
    quantity = models.IntegerField()
    product_id = models.IntegerField()

    def __str__(self):
        return str(self.batch_no)


class Staff(models.Model):
    id = models.AutoField(primary_key=True)
    aadhar_no = models.BigIntegerField()
    phone_no = models.BigIntegerField()
    staff_id = models.IntegerField()
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    addr_line_1 = models.CharField(max_length=25)
    addr_line_2 = models.CharField(max_length=25)
    job_designation = models.CharField(max_length=20)
    salary = models.IntegerField()
    join_date = models.DateField()

    def __str__(self):
        return str(self.first_name + ' ' + self.last_name)