import os

from django import forms

from django.contrib import admin
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from django.urls import path
from acme.products.models import Product
from acme.products.csv_import import csv_import_async


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


class ProductAdmin(admin.ModelAdmin):
    list_filter = ('is_active',)
    list_display = ('name', 'sku', 'description', 'is_active')
    search_fields = ('name', 'sku', 'description')
    change_list_template = "products/product_changelist.html"


    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
            path('delete-all/', self.delete_all),
        ]
        return my_urls + urls

    def import_csv(self, request):
        """
        Function to import csv
        Uses a form to upload the csv, and performs a product creation or
        update based on whether the sku exists in the database
        """
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]

            upload_to = os.path.join(request.user.username,
                                     'csv_imports', csv_file.name)
            file_name = default_storage.save(upload_to, csv_file)
            task = csv_import_async.delay(file_name, request.user.username)

            self.message_user(
                request,
                f"Your CSV is being imported, task_id : {task.task_id}")
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "products/csv_form.html", payload
        )

    def delete_all(self, request):
        """
        Custom method to delete all products.
        """
        if request.method == "POST":
            Product.objects.all().delete()
            self.message_user(request, "All products have been deleted")
            return redirect("..")
        return render(
            request, "products/delete_all.html",
        )

admin.site.register(Product, ProductAdmin)
