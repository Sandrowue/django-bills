from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class OwnedModel(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    class Meta:
        abstract = True

class Document(TimestampModel, OwnedModel):
    class Type(models.TextChoices):
        BILL = ("BILL", _("Lasku"))
        RECEIPT = ("RECEIPT", _("Kuitti"))
        CALCULATION = ("CALCULATION", _("Laskelma"))
        OTHER = ("OTHER", _("Muu"))

    type = models.CharField(max_length=20, choices=Type.choices)
    file = models.FileField(upload_to="docs/%Y-%m/")
   
class Category(TimestampModel, OwnedModel):
    name: models.CharField(max_length=100)
    parent = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        related_name="children",
        on_delete=models.CASCADE,
    )
   
class Account(TimestampModel, OwnedModel):
    name = models.CharField(max_length=100)
    bank_account = models.CharField(max_length=50, null=True, blank=True)


class Transaction(TimestampModel):
    class Type(models.TextChoices):
        INCOME = ("INCOME", _("Tulo"))
        EXPENSE = ("EXPENSE", _("Meno"))
    
    class State(models.TextChoices):
        UPCOMING = ("UPCOMING", _("Tuleva"))
        DONE = ("DONE", _("Tapahtumat"))

    account = models.ForeignKey(Account, on_delete=models.RESTRICT)
    type = models.CharField(max_length=20, choices=Type.choices)
    state = models.CharField(max_length=20, choices=State.choices)
    date = models.DateField()
    Category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL
    )
    documents = models.ManyToManyField(Document, related_name="transactions", blank=True,)

