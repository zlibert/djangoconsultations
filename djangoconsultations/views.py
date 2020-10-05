from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden


def home(request):
    context = {}
    return render(request, 'home.html', context)
