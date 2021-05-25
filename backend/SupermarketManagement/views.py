import datetime

from django.shortcuts import render
from SupermarketManagement import models


def dashboard(request):
    AllOrders = models.Order.objects.filter(order_date=datetime.date.today())
    CountOrders = models.Order.objects.count()
    CountCustomers = models.Customer.objects.count()
    ProductsOFS = models.Product.objects.filter(available_stock__lte=10)

    products_sold = models.OrderedItems.objects.all()
    income = 0
    for product in products_sold:
        product_reqd = models.Product.objects.get(product_id=product.product_id)
        income = income + product.quantity * product_reqd.price


    procured_items = models.ProcuredItems.objects.all()
    expense = 0

    for item in procured_items:
        product_reqd = models.Product.objects.get(product_id=item.product_id)
        expense = expense + item.quantity * product_reqd.price

    context = {'AllOrders': AllOrders, 'CountOrders': CountOrders, 'CountCustomers': CountCustomers,
               'ProductsOFS': ProductsOFS, 'income': income, 'expense': expense}

    return render(request, 'index.html', context)


def customer(request):
    AllCustomers = models.Customer.objects.all()
    context = {'customers' : AllCustomers}
    return render(request, 'customers.html', context)


def inventory(request):
    AllProducts = models.Product.objects.all()
    context = {'products' : AllProducts}

    return render(request, 'inventory.html', context)


def order(request):
    if request.method == "POST":
        batch_no = request.POST["batch_no"]
        bill_no = request.POST["bill_no"]
        product_id = request.POST['product_id']
        quantity = request.POST['quantity']
        amount_to_pay = request.POST['total_amount']
        delivery_date = request.POST['delivery_date']

        obj_procurement = models.Procurement(batch_no=batch_no, bill_no=bill_no, amount_to_pay=amount_to_pay,
                                             delivery_date=delivery_date)
        obj_procureditems = models.ProcuredItems(product_id=product_id, batch_no=batch_no, quantity=quantity)

        obj_procurement.save()
        obj_procureditems.save()

    return render(request, 'orders.html')


def purchase_return(request):
    if request.method == "POST":
        batch_no = request.POST["batch_no"]
        product_id = request.POST['product_id']
        amount_returned = request.POST['amount_returned']
        date = datetime.date.today()

        obj_purchasereturn = models.PurchaseReturn(batch_no=batch_no, product_id=product_id,
                                                   amount_returned=amount_returned, date=date)
        obj_purchasereturn.save()

    return render(request, 'purchase.html')


def sales_return(request):
    if request.method == "POST":
        product_id = request.POST['product']
        quantity = request.POST['quantity']
        order_id = request.POST['order_id']
        replacement_order_id = request.POST['r_order_id']
        amount_to_pay = request.POST['amount']
        obj = models.SalesReturn(product_id=product_id, quantity=quantity, order_id=order_id,
                                 replacement_order_id=replacement_order_id, amount_to_pay=amount_to_pay)
        obj.save()
        print("Data has been saved")
    return render(request, 'sales.html')


def staff(request):
    AllStaffs = models.Staff.objects.all()
    context = {'AllStaffs' : AllStaffs}
    return render(request, 'staffs.html', context)


def transaction(request):
    if request.method == "POST":
        order_id = request.POST["order_id"]
        staff_id = request.POST['staff_id']
        customer_ph_no = request.POST['customer_ph_no']
        brand = request.POST['brand']
        product_id = request.POST['product_id']
        quantity = request.POST['quantity']
        mode_of_payment = request.POST['mode_of_payment']
        amount_paid = request.POST['amount_to_pay']
        change_generated = request.POST['change_generated']
        pts_added_or_redeemed = request.POST['pts_added']

        obj_orders = models.Order(staff_id=staff_id, customer_ph_no=customer_ph_no, order_id=order_id,
                                  mode_of_payment=mode_of_payment, order_date=datetime.date.today())
        obj_ordereditems = models.OrderedItems(order_id=order_id,
                                               product_id=product_id, quantity=quantity)

        obj_invoice = models.Invoice(order_id=order_id, amount_paid=amount_paid,
                                     change_generated=change_generated)

        obj_membership = models.Membership(customer_ph_no=customer_ph_no, order_id=order_id,
                                           pts_added_or_redeemed = pts_added_or_redeemed)

        obj_orders.save()
        obj_ordereditems.save()
        obj_invoice.save()
        obj_membership.save()
        print("Data has been saved")

    return render(request, 'transaction.html')