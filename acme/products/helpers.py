import unicodecsv as ucsv
import requests
from acme.celery import app
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from acme.products.models import Product, Webhook

@app.task()
def csv_import_async(file_name, user_name=None):
    with default_storage.open(file_name) as csv_file:
        if user_name:
            user = User.objects.get(username=user_name)
        processed = 0
        csv_reader = ucsv.DictReader(csv_file, encoding='utf-8-sig')
        for row in csv_reader:
            product, created = Product.objects.get_or_create(
                sku=row.get('sku'))
            product.name = row.get('name')
            product.description = row.get('description')
            product.created_by = user
            product.save()
            processed +=1
        return {"processed_products": processed}

@app.task()
def post_to_webhooks(product_sku):
    product = Product.objects.get(sku=product_sku)
    product_json = {
        "name": product.id,
        "sku": product.sku,
        "description": product.description,
        "active":product.active
    }
    active_webhooks = Webhook.objects.filter(active=True)
    for webhook in active_webhooks:
        headers = {"Content-Type": "application/json"}
        requests.post(webhook.url, headers=headers, data=product_json)

    return