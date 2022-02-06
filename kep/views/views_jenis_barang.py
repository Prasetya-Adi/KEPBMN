# Create your views here.
import csv
import imp
from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from django.core.paginator import Paginator

from ..models import NomorSkep, JenisBarang, Barang
from ..forms import JenisBarangForms, TambahBarangForms

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test

from .views_decorator import checkPabean, checkP2

from django.db.models import Sum, Count
from django.db.models import F

import datetime

# Create and List Jenis Barang


@user_passes_test(checkP2)
def jenisbarang(request):
    form = JenisBarangForms(request.POST)
    jenis_barang_list = JenisBarang.objects.all()
    data = {
        'jenis_barang_list': jenis_barang_list,
        'form': form,
        'jenis_barang': True
    }

    if request.method == 'GET':
        return render(request, 'kep/jenis_barang/jenis_barang_list.html', data)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('jenis-barang-list'))

# Delete Jenis Barang


@user_passes_test(checkP2)
def jenisbarang_delete(request, id):
    jb = get_object_or_404(JenisBarang, id=id)
    if request.method == 'POST':
        jb.delete()
        return HttpResponseRedirect(reverse('jenis-barang-list'))
    return render(request, "kep/bdn/delete.html")

# Update Jenis Barang


@user_passes_test(checkP2)
def jenisbarang_update(request, id):
    jb = get_object_or_404(JenisBarang, id=id)
    form = JenisBarangForms(request.POST or None, instance=jb)
    context = {'form': form, 'menu_bdn': True}

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('jenis-barang-list'))

    return render(request, "kep/jenis_barang/jenis_barang_update.html", context)
