from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("luotu"),)


    class Meta:
        abstract = True

class OwnedModel(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("omistaja"),
    )

    class Meta:
        abstract = True

class Document(TimestampModel, OwnedModel):
    class Type(models.TextChoices):
        BILL = ("BILL", _("Lasku"))
        RECEIPT = ("RECEIPT", _("Kuitti"))
        CALCULATION = ("CALCULATION", _("Laskelma"))
        OTHER = ("OTHER", _("Muu"))

    type = models.CharField(max_length=20, choices=Type.choices, verbose_name=_("tyyppi"))
    name = models.CharField(max_length=100, blank=True, verbose_name=_("nimi"))
    file = models.FileField(upload_to="docs/%Y-%m/", verbose_name=_("tiedosto"))

    class Meta:
        verbose_name = _("dokumentti")
        verbose_name_plural = _("dokumentit")

    def __str__(self):
        return self.name if self.name else f"Document {self.id}"
   
class Category(TimestampModel, OwnedModel):
    name: models.CharField(max_length=100, verbose_name=_("nimi"),)
    parent = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        related_name="children",
        on_delete=models.CASCADE,
        verbose_name=_("yläkategoria"),
    )

    class Meta:
        verbose_name = _("kategoria")
        verbose_name_plural = _("kategoriat")

    def __str__(self):
        prefix = f"{self.parent} / " if self.parent else ""
        return f"{prefix}{self.name}"
   
class Account(TimestampModel, OwnedModel):
    name = models.CharField(max_length=100, verbose_name=_("nimi"),)
    bank_account = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("pankkitili"),)

    class Meta:
        verbose_name = _("tili")
        verbose_name_plural = _("tilit")
    def __str__(self):
        return f"{self.id:04d} {self.name}"


class Transaction(TimestampModel):
    class Type(models.TextChoices):
        INCOME = ("INCOME", _("Tulo"))
        EXPENSE = ("EXPENSE", _("Meno"))
    
    class State(models.TextChoices):
        UPCOMING = ("UPCOMING", _("Tuleva"))
        DONE = ("DONE", _("Tapahtumat"))

    account = models.ForeignKey(Account, on_delete=models.RESTRICT, verbose_name=_("tili"),)
    type = models.CharField(max_length=20, choices=Type.choices, verbose_name=_("tyyppi"),)
    state = models.CharField(max_length=20, choices=State.choices, verbose_name=_("tila"),)
    date = models.DateField(verbose_name=_("päiväys"),)
    amount = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_("määrä"),)    
    comment = models.CharField(max_length=200, blank=True, verbose_name=_("kommentti")) 
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_("kategoria"),
    )
    documents = models.ManyToManyField(Document, related_name="transactions", blank=True, verbose_name=_("dokumentit"),)
    
    class Meta:
        verbose_name = ("tilitapahtuma")
        verbose_name_plural = _("tilitapahtumat")

    def __str__(self):
        return (
            f"{self.date} {self.amount:8.2f} "
            f"{self.comment} ({self.State(self.State).label})"
        )
    

# lukutyypit:
#   int = konkonaisluku, esim. 1,5,7, 11 tai 0, -3
#   float = liukuluku, esim. 1.0, 2.6, 3.83, -0.8
#   Decimal = desimaaliluku, esim. Decimal('0.1'), Decimal('-11.8')
# from decimal import Decimal



