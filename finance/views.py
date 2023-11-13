from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView, View

from .models import Account, Document

# Create your views here.
@login_required
def frontpage(request):
    return render(request, "finance/index.html")

class AccountView(View):
    model = Account

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

class AccountsList(LoginRequiredMixin, AccountView, ListView):
    pass
   
class AccountDetail(LoginRequiredMixin, DetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["transactions"] = self.object.transactions.all()
        return context

@login_required
def documents(request):
    context = {
        "documents": Document.objects.filter(owner=request.user),
    }
    return render(request, "finance/documents.html", context)
