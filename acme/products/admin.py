from django.http import HttpResponse
from django import forms
import boto3
import json
from botocore.client import Config

from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path
from acme.products.models import Product, Webhook
from acme.products.helpers import csv_import_async, post_to_webhooks
from acme.constants import ACME_S3_BUCKET

class CsvImportForm(forms.Form):
    csv_file = forms.FileField(required=False)


class ProductAdmin(admin.ModelAdmin):
    list_filter = ('active',)
    list_display = ('name', 'sku', 'description', 'active')
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

        if request.GET:
            """
            Sends file to s3 bucket
            """
            file_name = request.GET['file_name']
            file_type = request.GET['file_type']
            S3_BUCKET = ACME_S3_BUCKET
            s3 = boto3.client(
                's3',
                config=Config(
                    signature_version='s3v4',
                    region_name='us-east-2'
                )
            )
            presigned_post = s3.generate_presigned_post(
                Bucket=S3_BUCKET,
                Key=file_name,
                Fields={"acl": "public-read", "Content-Type": file_type},
                Conditions=[
                    {"acl": "public-read"},
                    {"Content-Type": file_type}
                ],
                ExpiresIn=3600
            )
            resp_data = json.dumps({
                'data': presigned_post,
                'url': 'https://%s.s3.amazonaws.com/%s' % (
                    S3_BUCKET, file_name)
            })
            return HttpResponse(resp_data)

        if request.method == "POST":
            """
            Triggers importing csv from s3 bucket
            """
            file_name = request.POST['file-name']
            csv_import_async.delay(file_name, request.user.username)

            self.message_user(
                request,
                f"Your CSV is being imported")
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

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        post_to_webhooks.delay(obj.sku)


class WebhookAdmin(admin.ModelAdmin):
    list_filter = ('active',)
    list_display = ('url',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Webhook, WebhookAdmin)
