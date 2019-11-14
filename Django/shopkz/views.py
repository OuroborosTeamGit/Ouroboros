
from django.http import HttpResponse, Http404, HttpResponseRedirect, request
from .models import *
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic.edit import CreateView


from django.shortcuts import render, get_object_or_404

def index(request):
    return render(request , "shopkz/index.html")

def checkout(request):
    """Using get_object_or_404() shortcut to return PNF 404"""
    return render(request, "shopkz/checkout.html")


def addGood(request):
    return render(request ,"shopkz/addGood.html")