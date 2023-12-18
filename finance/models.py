from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy

class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"),)


    class Meta:
        abstract = True

class OwnedModel(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("owner"),
    )

    class Meta:
        abstract = True

class Document(TimestampModel, OwnedModel):
    class Type(models.TextChoices):
        BILL = ("BILL", _("Bill"))
        RECEIPT = ("RECEIPT", _("Receipt"))
        CALCULATION = ("CALCULATION", _("Calculation"))
        OTHER = ("OTHER", _("Other"))

    type = models.CharField(max_length=20, choices=Type.choices, verbose_name=_("type"))
    name = models.CharField(max_length=100, blank=True, verbose_name=_("name"))
    file = models.FileField(upload_to="docs/%Y-%m/", verbose_name=_("file"))

    class Meta:
        verbose_name = _("document")
        verbose_name_plural = _("documents")

    def __str__(self):
        return self.name if self.name else f"Document {self.id}"
   
class Category(TimestampModel, OwnedModel):
    name = models.CharField(max_length=100, verbose_name=_("name"),)
    parent = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        related_name="subcategories",
        on_delete=models.CASCADE,
        verbose_name=_("parent category"),
    )

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self, level=0):
        if self.parent and level < 20:
            parent_str = self.parent.__str__(level=level + 1)
        elif self.parent:
            parent_str = "..."
        else:   
            parent_str = ""
        prefix = f"{parent_str} / " if parent_str else ""
        return f"{prefix}{self.name}"
    
    def get_absolute_url(self):
        return reverse("category-detail", kwargs={"pk": self.pk})
    
    defaults = [ # Default Categories
    # key, parent_key, name
    ("exp", None, _("Expenses")),
    ("living", "exp", _("Living Costs")),
    ("food", "living", _("Food")),
    ("income", None, pgettext_lazy("category name", "Income")),
    ("salary", "income", _("Salary")),
    ]

    @classmethod
    def create_defaults(cls, owner):
        key_to_id = {}
        for key, parent_key, name in cls.defaults:
            parent_id = key_to_id[parent_key] if parent_key else None
            category = cls.objects.update_or_create(
                name=name,
                owner=owner,
                parent_id=parent_id
            )[0]
            key_to_id[key] = category.id
   
class Account(TimestampModel, OwnedModel):
    name = models.CharField(max_length=100, verbose_name=_("name"),)
    bank_account = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("bank account"),)

    class Meta:
        verbose_name = _("account")
        verbose_name_plural = _("accounts")
    def __str__(self):
        return f"{self.id:04d} {self.name}"
    
    def get_absolute_url(self):
        return reverse("account-detail", kwargs={"pk": self.pk})
    


class Transaction(TimestampModel):
    class Type(models.TextChoices):
        INCOME = ("INCOME", _("Income"))
        EXPENSE = ("EXPENSE", _("Expense"))
    
    class State(models.TextChoices):
        UPCOMING = ("UPCOMING", _("Upcoming"))
        DONE = ("DONE", _("Done"))

    account = models.ForeignKey(Account, on_delete=models.RESTRICT, related_name="transactions", verbose_name=_("account"),)
    type = models.CharField(max_length=20, choices=Type.choices, verbose_name=_("type"),)
    state = models.CharField(max_length=20, choices=State.choices, verbose_name=_("state"),)
    date = models.DateField(verbose_name=_("date"),)
    amount = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_("amount"),)    
    comment = models.CharField(max_length=200, blank=True, verbose_name=_("comment"),) 
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_("category"),
    )
    documents = models.ManyToManyField(Document, related_name="transactions", blank=True, verbose_name=_("documents"),)
    
    class Meta:
        verbose_name = _("transaction")
        verbose_name_plural = _("transactions")

    def __str__(self):
        return (
            f"{self.date} {self.amount:8.2f} "
            f"{self.comment} ({self.State(self.state).label})"
        )
    

# lukutyypit:
#   int = konkonaisluku, esim. 1,5,7, 11 tai 0, -3
#   float = liukuluku, esim. 1.0, 2.6, 3.83, -0.8
#   Decimal = desimaaliluku, esim. Decimal('0.1'), Decimal('-11.8')
# from decimal import Decimal



