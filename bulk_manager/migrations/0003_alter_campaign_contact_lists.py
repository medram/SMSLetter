# Generated by Django 3.2 on 2021-05-18 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0013_alter_contactlist_options'),
        ('bulk_manager', '0002_campaign_contact_lists'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='contact_lists',
            field=models.ManyToManyField(blank=True, to='sms.ContactList', verbose_name='Contact Lists'),
        ),
    ]
