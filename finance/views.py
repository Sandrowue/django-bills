from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import Account, Document

# Create your views here.
@login_required
def frontpage(request):
    return render(request, "finance/index.html")

@login_required
def accounts(request):
    context = {
        "accounts": Account.objects.filter(owner=request.user),
    }
    return render(request, "finance/accounts.html", context)

@login_required
def documents(request):
    context = {
        "documents": Document.objects.filter(owner=request.user),
    }
    return render(request, "finance/documents.html", context)
