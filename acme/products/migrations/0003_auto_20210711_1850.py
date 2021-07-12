# Generated by Django 3.2.5 on 2021-07-11 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Webhook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('url', models.URLField()),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.RenameField(
            model_name='product',
            old_name='is_active',
            new_name='active',
        ),
        migrations.AddField(
            model_name='product',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]