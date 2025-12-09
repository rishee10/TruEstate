from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django import forms
from django.db import transaction
import csv, io
from .models import Customer, Product, Tag, Sale

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'name', 'phone_number', 'region')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'name', 'brand', 'category')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)




@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'date', 'customer', 'product', 'final_amount')
    change_list_template = "admin/sales_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'import-csv/',
                self.admin_site.admin_view(self.import_csv),
                name='sales_import_csv'
            ),
        ]
        return custom_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            form = CSVUploadForm(request.POST, request.FILES)
            if form.is_valid():

                f = form.cleaned_data["csv_file"]
                data = io.TextIOWrapper(f.file, encoding="utf-8")
                reader = list(csv.DictReader(data))

                from dateutil import parser

                BATCH_SIZE = 500

                # ---------------- CACHE EXISTING DATA ----------------
                customers_cache = {c.customer_id: c for c in Customer.objects.all()}
                products_cache = {p.product_id: p for p in Product.objects.all()}
                tags_cache = {t.name: t for t in Tag.objects.all()}
                existing_sales = set(
                    Sale.objects.values_list("transaction_id", flat=True)
                )

                new_customers = []
                new_products = []
                new_sales = []
                product_tags_map = {}

                # ---------------- STEP 1: COLLECT CUSTOMERS & PRODUCTS ----------------
                for row in reader:

                    # ---------- CUSTOMER ----------
                    cid = row["Customer ID"].strip()
                    if cid not in customers_cache:
                        c = Customer(
                            customer_id=cid,
                            name=row["Customer Name"],
                            phone_number=row["Phone Number"],
                            gender=row.get("Gender"),
                            age=int(float(row["Age"])) if row.get("Age") else None,
                            region=row.get("Customer Region"),
                            customer_type=row.get("Customer Type"),
                        )
                        new_customers.append(c)
                        customers_cache[cid] = c

                    # ---------- PRODUCT ----------
                    pid = row["Product ID"].strip()
                    if pid not in products_cache:
                        p = Product(
                            product_id=pid,
                            name=row["Product Name"],
                            brand=row.get("Brand"),
                            category=row.get("Product Category"),
                        )
                        new_products.append(p)
                        products_cache[pid] = p

                        product_tags_map[pid] = [
                            t.strip() for t in row.get("Tags", "").split(",") if t.strip()
                        ]

                # ---------------- STEP 2: BULK INSERT CUSTOMERS & PRODUCTS ----------------
                Customer.objects.bulk_create(new_customers, ignore_conflicts=True)
                Product.objects.bulk_create(new_products, ignore_conflicts=True)

                # ---------------- STEP 3: REFRESH SAVED OBJECTS ----------------
                customers_cache = {c.customer_id: c for c in Customer.objects.all()}
                products_cache = {p.product_id: p for p in Product.objects.all()}

                # ---------------- STEP 4: PREPARE SALES ----------------
                for row in reader:

                    tx_id = str(row["Transaction ID"])
                    if tx_id in existing_sales:
                        continue

                    try:
                        date = parser.parse(row["Date"], dayfirst=True).date()
                    except:
                        continue

                    cid = row["Customer ID"].strip()
                    pid = row["Product ID"].strip()

                    s = Sale(
                        transaction_id=tx_id,
                        date=date,
                        customer=customers_cache[cid],
                        product=products_cache[pid],
                        quantity=int(float(row["Quantity"])),
                        price_per_unit=float(row["Price per Unit"]),
                        discount_percentage=float(row.get("Discount Percentage", 0)),
                        total_amount=float(row.get("Total Amount")),
                        final_amount=float(row.get("Final Amount")),
                        payment_method=row.get("Payment Method"),
                        order_status=row.get("Order Status"),
                        delivery_type=row.get("Delivery Type"),
                        store_id=row.get("Store ID"),
                        store_location=row.get("Store Location"),
                        salesperson_id=row.get("Salesperson ID"),
                        employee_name=row.get("Employee Name"),
                    )
                    new_sales.append(s)

                    if len(new_sales) >= BATCH_SIZE:
                        Sale.objects.bulk_create(new_sales, ignore_conflicts=True)
                        new_sales.clear()

                # ---------------- STEP 5: FINAL BULK INSERT SALES ----------------
                Sale.objects.bulk_create(new_sales, ignore_conflicts=True)

                # ---------------- STEP 6: TAG M2M ASSIGNMENT ----------------
                for pid, tag_list in product_tags_map.items():
                    product = products_cache[pid]

                    for tag_name in tag_list:
                        if tag_name not in tags_cache:
                            tag_obj = Tag.objects.create(name=tag_name)
                            tags_cache[tag_name] = tag_obj

                        product.tags.add(tags_cache[tag_name])

                self.message_user(
                    request,
                    "✅ 10K+ CSV imported successfully (Optimized Bulk Mode)."
                )
                return redirect("..")

        else:
            form = CSVUploadForm()

        return render(
            request,
            "admin/csv_upload.html",
            {"form": form}
        )
