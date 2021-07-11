import unicodecsv as ucsv
from acme.celery import app
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from acme.products.models import Product

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