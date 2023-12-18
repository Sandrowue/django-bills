from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, FormView, DeleteView
from django.urls import reverse_lazy

from .models import Account, Category, Document, Transaction

# Create your views here.
@login_required
def frontpage(request):
    return render(request, "finance/index.html")

class OwnerFilteredMixin(LoginRequiredMixin):
    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)
    
class OwnerAutoFillingCreateView(OwnerFilteredMixin, CreateView):
    def form_valid(self, form):
        form.save(commit=False)
        if not form.instance.owner_id:
            form.instance.owner = self.request.user
        return super().form_valid(form)

class AccountList(OwnerFilteredMixin, ListView):
    model = Account
   
class AccountDetail(LoginRequiredMixin, DetailView):
    model = Account
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["transactions"] = self.object.transactions.all()
        return context
    
class AccountCreate(OwnerAutoFillingCreateView):
    model = Account
    fields = ["name", "bank_account"]

class AccountDelete(OwnerFilteredMixin, DeleteView):
    model = Account
    success_url = reverse_lazy("accounts")

class DocumentList(OwnerFilteredMixin, ListView):
    model = Document

class DocumentDetail(OwnerFilteredMixin, DetailView):
    model = Document

class CategoryList(OwnerFilteredMixin, ListView):
    model = Category

class CategoryDetail(OwnerFilteredMixin, DetailView):
    model = Category

class CategoryCreate(OwnerAutoFillingCreateView):
    model = Category
    fields = ["name", "parent"]

class CategoryDelete(OwnerFilteredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy("categories")

class CreateDefaultCategoriesForm(forms.Form):
    pass

class CreateDefaultCategoriesFormView(FormView):
    form_class = CreateDefaultCategoriesForm
    template_name = "finance/category_create_defaults_form.html"
    success_url = reverse_lazy("categories")

    def form_valid(self, form):
        Category.create_defaults(owner=self.request.user)
        return super().form_valid(form)
    
class TransactionCreate(CreateView):
    model = Transaction
    fields = [
        "type",
        "state",
        "date",
        "amount",
        "comment",
        "category",
        "documents",
    ]

    def form_valid(self, form):
        # Täytetään luotavaan tilitapahtumaan tilin id
        form.save(commit=False)
        if not form.instance.account_id:
            # Tilin id tulee tänne URL-parametrina (ks. urls.py)
            form.instance.account_id = self.kwargs["account_id"]
        return super().form_valid(form)
    
    def get_success_url(self):
        # Paluuosoite, johon palataan kun tilitapatuma on luotu.
        # Haetaan sen tilin detail-näkymä, johon luotu tilitapahtuma liittyy
        return reverse_lazy(
            "account-detail",
            kwargs={"pk": self.kwargs["account_id"]},
        )



