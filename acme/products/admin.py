import unicodecsv as ucsv
from django import forms

from django.contrib import admin

from django.shortcuts import render, redirect
from django.urls import path
from acme.products.models import Product



class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


class ProductAdmin(admin.ModelAdmin):

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
            csv_reader = ucsv.DictReader(csv_file, encoding='utf-8-sig')
            for row in csv_reader:
                Product.objects.update_or_create(
                        sku=row.get('sku'), name=row.get('name'),
                        description=row.get('description'))
            self.message_user(request, "Your csv file has been imported")
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
