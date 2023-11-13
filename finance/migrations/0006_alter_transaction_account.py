# Generated by Django 4.2.6 on 2023-11-13 15:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0005_alter_account_options_alter_category_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='transactiens', to='finance.account', verbose_name='account'),
        ),
    ]
