from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Account, Category, Document, Transaction

# Register your models here.

@admin.register(Document)
class AccountAdmin(ModelAdmin):
    pass

@admin.register(Category)
class AccountAdmin(ModelAdmin):
    list_display = [
        "id",
        "__str__",
        "created_at"
    ]
    list_display_links = list_display


@admin.register(Account)
class AccountAdmin(ModelAdmin):
    pass

@admin.register(Transaction)
class AccountAdmin(ModelAdmin):
    list_display = [
        "id",
        "account",
        "date",
        "amount",
        "type",
        "state",
        "category",
        "comment",
    ]
    list_display_links = list_display