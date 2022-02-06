from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test, login_required
from .views_decorator import checkPabean, checkP2

from ..models import NomorSkep, JenisBarang, Barang
from ..forms import TambahBarangForms


@user_passes_test(checkP2)
def tambah_barang_bdn(request, id):
    skep = get_object_or_404(NomorSkep, id=id)
    form = TambahBarangForms(request.POST or None)
    context = {'form': form, 'bdn': skep, 'menu_bdn': True}

    if request.method == 'GET':
        return render(request, 'kep/bdn/tambah_barang.html', context)

    if request.method == 'POST':
        if form.is_valid():
            barang = form.save(commit=False)
            barang.nomor_skep = skep
            barang.save()

        return HttpResponseRedirect(reverse('detail-bdn', args=[skep.id]))


@user_passes_test(checkP2)
def update_barang_bdn(request, id):
    barang = get_object_or_404(Barang, id=id)
    skep = barang.nomor_skep
    form = TambahBarangForms(request.POST or None, instance=barang)
    context = {'form': form, 'barang': barang, 'menu_bdn': True}

    if request.method == 'GET':
        return render(request, 'kep/bdn/tambah_barang.html', context)

    if request.method == 'POST':
        if form.is_valid():
            barang = form.save(commit=False)
            barang.nomor_skep = skep
            barang.save()
            return HttpResponseRedirect(reverse('detail-bdn', args=[skep.id]))


@user_passes_test(checkP2)
def barang_delete(request, id):
    barang = get_object_or_404(Barang, id=id)
    skep = barang.nomor_skep
    if request.method == 'POST':
        barang.delete()
        return HttpResponseRedirect(reverse('detail-bdn', args=[skep.id]))
    return render(request, "kep/bdn/delete.html")
