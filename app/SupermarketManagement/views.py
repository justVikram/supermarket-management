import datetime
from django.http import JsonResponse
from django.shortcuts import render
from SupermarketManagement import models
from django.db.models import Sum, Count
import pandas as pd
from django.db.models.functions import TruncMonth

procurement_amount = 0
sales_return_amount = 0
purchase_return_amount = 0

count = 0
count_txn = 0
count_sales = 0

total_sales_amount = 0
total_purchase_amount = 0


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
    context = {'customers': AllCustomers}
    return render(request, 'customers.html', context)


def inventory(request):
    AllProducts = models.Product.objects.filter(available_stock__gt=10)
    context = {'products': AllProducts}

    return render(request, 'inventory.html', context)


def order(request):
    AllAgencies = models.Supplier.objects.order_by('supplier_ph_no').distinct()
    AllBrands = models.Product.objects.order_by('brand').values_list('brand', flat=True).distinct()
    context = {'AllAgencies': AllAgencies, 'AllBrands': AllBrands}

    if request.method == "POST":
        batch_no = request.POST["batch_no"]
        bill_no = request.POST["bill_no"]
        amount_to_pay = request.POST['total_amount']
        delivery_date = request.POST['delivery_date']
        agency = request.POST['agency']

        ph_no = models.Supplier.objects.filter(agency_name=agency).get().supplier_ph_no

        models.Procurement.objects.filter(batch_no=batch_no).update(bill_no=bill_no, amount_to_pay=amount_to_pay,
                                                                    delivery_date=delivery_date, supplier_ph_no=ph_no)

        global procurement_amount
        procurement_amount = 0

        global count
        count = 0

    return render(request, 'orders.html', context)


def purchase_return(request):
    AllBatchNo = models.ProcuredItems.objects.order_by('batch_no').values_list('batch_no', flat=True).distinct()
    context = {'ALlBatchNo': AllBatchNo}
    if request.method == "POST":
        batch_no = request.POST["batch_no"]

        global total_purchase_amount
        total_purchase_amount = 0

        models.ProcuredItems.objects.filter(batch_no=batch_no).delete()

    return render(request, 'purchase.html', context)


def sales_return(request):
    AllOrders = models.Order.objects.order_by('order_id')
    context = {'AllOrders': AllOrders}

    if request.method == "POST":
        order_id = request.POST['order_id']
        replacement_order_id = request.POST['r_order_id']

        models.SalesReturn.objects.filter(order_id=order_id).update(replacement_order_id=replacement_order_id)

        global total_sales_amount
        total_sales_amount = 0

    return render(request, 'sales.html', context)


def staff(request):
    AllStaffs = models.Staff.objects.all()
    context = {'AllStaffs': AllStaffs}
    return render(request, 'staffs.html', context)


def transaction(request):
    AllBrands = models.Product.objects.order_by('brand').values_list('brand', flat=True).distinct()

    AllProducts = models.Product.objects.order_by('product_name').all()

    ProductsToBeDisplayed = models.Product.objects.order_by('product_id').all()

    next_order_id = models.Order.objects.count() + 1

    AllStaffs = models.Staff.objects.all().order_by('staff_id')

    context = {'AllBrands': AllBrands, 'next_order_id': next_order_id, 'AllStaffs': AllStaffs,
               'AllProducts': AllProducts, 'ProductsToDisplay': ProductsToBeDisplayed}

    if request.method == "POST":
        order_id = next_order_id - 1
        staff_id = request.POST['staff_id']
        customer_ph_no = request.POST['customer_ph_no']
        product_id = request.POST['product_id']
        quantity = request.POST['quantity']
        mode_of_payment = request.POST['mode_of_payment']
        amount_paid = request.POST['amount_to_pay']
        pts_added_or_redeemed = float(amount_paid) * 0.1

        models.Membership.objects.filter(customer_ph_no=customer_ph_no).delete()

        obj_customer = models.Customer(customer_ph_no=customer_ph_no)

        if not models.Customer.objects.filter(customer_ph_no=customer_ph_no).exists():
            obj_customer.save()

        # OLD NEW CODE HERE
        models.Order.objects.filter(order_id=order_id).update(staff_id=staff_id, customer_ph_no=customer_ph_no,
                                                              mode_of_payment=mode_of_payment,
                                                              order_date=datetime.date.today())

        models.Invoice.objects.filter(order_id=order_id).update(amount_paid=amount_paid, change_generated=0)
        models.Membership.objects.filter(order_id=order_id).update(customer_ph_no=customer_ph_no,
                                                                   pts_added_or_redeemed=pts_added_or_redeemed)

        print("Data has been saved")

        global amount
        amount = 0

        global count_txn
        count_txn = 0

    return render(request, 'transaction.html', context)


amount = 0


def show_added_products(request):
    if request.method == 'POST':
        product_id = request.POST['product_id']
        quantity = request.POST['quantity']
        ph_no = request.POST['ph_no']
        price = int(models.Product.objects.get(product_id=product_id).price)
        name = models.Product.objects.get(product_id=product_id).product_name
        next_order_id = request.POST.get('order_id', False)
        order_id = next_order_id

        print(next_order_id)

        global amount
        amount += price * int(quantity)

        pts = list(models.Membership.objects.filter(customer_ph_no=ph_no).aggregate
                   (Sum('pts_added_or_redeemed')).values())[0]

        global count_txn
        count_txn = count_txn + 1

        if count_txn == 1:
            obj_order = models.Order(order_id=order_id)
            obj_order.save()
            obj_invoice = models.Invoice(order_id=order_id)
            obj_invoice.save()
            obj_membership = models.Membership(order_id=order_id)
            obj_membership.save()

        obj_ordereditem = models.OrderedItems(order_id=order_id, quantity=quantity, product_id=product_id)
        obj_ordereditem.save()

        old = models.Product.objects.filter(product_id=product_id)
        newstock = int(old.get().available_stock) - int(quantity)
        models.Product.objects.filter(product_id=product_id).update(available_stock=newstock)
        newquantity = int(old.get().quantity_sold) + int(quantity)
        models.Product.objects.filter(product_id=product_id).update(quantity_sold=newquantity)

        data = {
            'quantity': quantity,
            'pname': name,
            'price': price,
            'product_id': product_id,
            'amount': amount,
            'points': pts
        }
        return JsonResponse(data)


def chained_dropdown(request):
    if request.method == "POST":
        brand = request.POST['brand']
        print(brand)

        sort_by_brand = list(
            models.Product.objects.filter(brand=brand).order_by('product_id').values('product_id', 'product_name'))

        data = {
            'SortByBrand': sort_by_brand
        }
        return JsonResponse(data)


def show_supplier_info(request):
    if request.method == "POST":
        agency = request.POST['agency']
        print(agency)

        SupplierInfo = models.Supplier.objects.filter(agency_name=agency).get()
        SupplierPhNo = SupplierInfo.supplier_ph_no
        SupplierAddr = SupplierInfo.addr_line_1

        data = {
            'ph_no': SupplierPhNo,
            'addr': SupplierAddr,
        }

        return JsonResponse(data)


def show_added_products_orders(request):
    if request.method == 'POST':
        product_id = request.POST['product_id']
        quantity = request.POST['quantity']
        batch_no = request.POST['batch_no']
        price = int(models.Product.objects.get(product_id=product_id).price)
        name = models.Product.objects.get(product_id=product_id).product_name

        global procurement_amount
        procurement_amount += price * int(quantity)

        global count
        count = count + 1

        if count == 1:
            obj_procurement = models.Procurement(batch_no=batch_no, delivery_date=datetime.date.today())
            obj_procurement.save()

        obj_procureditem = models.ProcuredItems(product_id=product_id, quantity=quantity, batch_no=batch_no)
        obj_procureditem.save()

        old = models.Product.objects.filter(product_id=product_id)
        newstock = int(old.get().available_stock) + int(quantity)
        models.Product.objects.filter(product_id=product_id).update(available_stock=newstock)

        data = {
            'quantity': quantity,
            'pname': name,
            'price': price,
            'product_id': product_id,
            'amount': procurement_amount,
        }
        return JsonResponse(data)


def chained_dropdown_orders(request):
    if request.method == "POST":
        brand = request.POST['brand']
        print(brand)

        sort_by_brand = list(
            models.Product.objects.filter(brand=brand).order_by('product_id').values('product_id', 'product_name'))

        data = {
            'SortByBrand': sort_by_brand
        }
        return JsonResponse(data)


def chained_dropdown_sales(request):
    if request.method == "POST":
        order_id = request.POST['order_id']
        print(order_id)

        sort_by_order = list(
            models.OrderedItems.objects.filter(order_id=order_id).order_by('product_id').values('product_id'))

        data = {
            'SortByOrder': sort_by_order
        }
        return JsonResponse(data)


def show_added_products_sales(request):
    if request.method == "POST":
        product_id = request.POST['product_id']
        quantity = request.POST['quantity']
        order_id = request.POST['order_id']
        price = int(models.Product.objects.get(product_id=product_id).price)
        name = models.Product.objects.get(product_id=product_id).product_name

        global sales_return_amount
        sales_return_amount += price * int(quantity)

        global total_sales_amount
        total_sales_amount += sales_return_amount

        obj = models.SalesReturn(product_id=product_id, quantity=quantity, order_id=order_id,
                                 amount_to_pay=sales_return_amount)
        obj.save()

        old = models.Product.objects.filter(product_id=product_id)
        newstock = int(old.get().available_stock) + int(quantity)
        models.Product.objects.filter(product_id=product_id).update(available_stock=newstock)
        newquantity = int(old.get().quantity_sold) - int(quantity)
        models.Product.objects.filter(product_id=product_id).update(quantity_sold=newquantity)

        data = {
            'quantity': quantity,
            'pname': name,
            'price': price,
            'product_id': product_id,
            'total_sales_amount': total_sales_amount,
            'sales_return_amount': sales_return_amount
        }
        return JsonResponse(data)


def chained_dropdown_purchase(request):
    if request.method == "POST":
        batch_no = request.POST['batch_no']
        print(batch_no)

        sort_by_batch = list(
            models.ProcuredItems.objects.filter(batch_no=batch_no).order_by('product_id').values('product_id'))

        data = {
            'SortByBatch': sort_by_batch
        }
        return JsonResponse(data)


def show_added_products_purchase(request):
    if request.method == "POST":
        product_id = request.POST['product_id']
        batch_no = request.POST['batch_no']
        price = int(models.Product.objects.get(product_id=product_id).price)
        name = models.Product.objects.get(product_id=product_id).product_name
        quantity = models.ProcuredItems.objects.get(batch_no=batch_no, product_id=product_id).quantity

        global purchase_return_amount
        purchase_return_amount += price * int(quantity)

        global total_purchase_amount
        total_purchase_amount += purchase_return_amount

        obj = models.PurchaseReturn(product_id=product_id, date=datetime.date.today(), batch_no=batch_no,
                                    amount_returned=purchase_return_amount)

        obj.save()

        old = models.Product.objects.filter(product_id=product_id)
        newstock = int(old.get().available_stock) - int(quantity)
        models.Product.objects.filter(product_id=product_id).update(available_stock=newstock)

        data = {
            'quantity': quantity,
            'pname': name,
            'price': price,
            'product_id': product_id,
            'total_purchase_amount': total_purchase_amount,
            'purchase_return_amount': purchase_return_amount
        }
        return JsonResponse(data)


def generatepdf(request, *args, **kwargs):
    reqd_id = kwargs.get('order_id')

    ordered_items = list(models.OrderedItems.objects.filter(order_id=reqd_id))
    amount_paid = models.Invoice.objects.get(order_id=reqd_id).amount_paid
    order_details = models.Order.objects.get(order_id=reqd_id)
    product_info = []

    for ordered_item in ordered_items:
        corresponding_prod_details = models.Product.objects.get(product_id=ordered_item.product_id)
        product_info.append(corresponding_prod_details)

    prod_details_w_quantity = zip(product_info, ordered_items)

    context = {
        'ordered_items': ordered_items,
        'amount_paid': amount_paid,
        'order_details': order_details,
        'product_info': product_info,
        'complete_list': prod_details_w_quantity
    }

    return render(request, 'invoice-pdf.html', context)


def generate_graphs(request):
    orders = models.Order.objects.all()
    sales = models.Invoice.objects.all()

    df = pd.DataFrame(
        {'date': orders.values_list('order_date', flat=True), 'amount': sales.values_list('amount_paid', flat=True)})
    revenue = df.groupby('date')['amount'].sum().reset_index()

    revenue['amount_sum'] = revenue['amount'].cumsum()

    context = {
        'products': models.Product.objects.values('product_name', 'brand', 'quantity_sold'),
        'orders': models.Order.objects.values('order_date').annotate(total=Count('order_id')).order_by('order_date'),
        'revenue': revenue
    }
    return render(request, 'graphs.html', context)
