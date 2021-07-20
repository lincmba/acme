import codecs
import csv

import boto3
import requests
from botocore.client import Config
from django.contrib.auth.models import User

from acme.celery import app
from acme.constants import ACME_S3_BUCKET
from acme.products.models import Product, Webhook


@app.task()
def csv_import_async(file_name, user_name=None):
    """
    Performs csv import in the background in the following steps
    - Imports csv file from s3 bucket
    - Reads file
    - Creates products from those in the csv file
    :param file_name: Name of file as stored in s3
    :param user_name: Current user's username
    :return:
    """
    s3 = boto3.client(
        's3',
        config=Config(
            signature_version='s3v4',
            region_name='us-east-2'
        )
    )
    obj = s3.get_object(Bucket=ACME_S3_BUCKET, Key=file_name)

    if user_name:
        user = User.objects.get(username=user_name)
    csv_reader = csv.DictReader(codecs.getreader("utf-8")(obj["Body"]))
    if 'sku' in csv_reader.fieldnames:
        for row in csv_reader:
            product, created = Product.objects.get_or_create(
                sku=row.get('sku'))
            product.name = row.get('name')
            product.description = row.get('description')
            product.created_by = user
            product.save()


@app.task()
def post_to_webhooks(product_sku):
    """
    Sends product data in json to all active webhooks
    :param product_sku:
    :return:
    """
    product = Product.objects.get(sku=product_sku)
    product_json = {
        "name": product.id,
        "sku": product.sku,
        "description": product.description,
        "active": product.active
    }
    active_webhooks = Webhook.objects.filter(active=True)
    for webhook in active_webhooks:
        headers = {"Content-Type": "application/json"}
        requests.post(webhook.url, headers=headers, data=product_json)
