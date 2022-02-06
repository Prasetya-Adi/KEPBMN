# Create your views here.
import csv
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from django.core.paginator import Paginator

from ..models import NomorSkep, Barang

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

import datetime

from django.db.models import Sum, Count, F
from django.db.models.functions import TruncMonth

from . import views_decorator


# Page Index after login is success with decorator login required and redirect to login url if force to get here


@ login_required(login_url='login')
def index(request):
    skep_list = NomorSkep.objects.all()
    bmn_list = NomorSkep.objects.all().filter(no_bmn__isnull=False)
    bdn_total = skep_list.count()
    bmn_total = bmn_list.count()

    # saldo
    barang_bmn = Barang.objects.all().filter(nomor_skep__no_bmn__isnull=False)
    bbbmn = barang_bmn.values(jb=F('jenis_barang__jenis_barang'), sat=F('jenis_barang__isi_satuan')).order_by(
        'jenis_barang__jenis_barang').annotate(total=Sum(F('jumlah_kemasan')*F('isi')))

    # Chart BMN
    bmn = bmn_list.annotate(month=TruncMonth('tanggal_bmn')).values(
        'month').annotate(total=Count('no_bmn'))

    labels_bmn = []
    data_bmn = []
    for i in bmn:
        labels_bmn.append(i['month'].strftime("%B"))
        data_bmn.append(i['total'])

    # Chart BDN
    bdn = skep_list.annotate(month=TruncMonth('tanggal_bdn')).values(
        'month').annotate(total=Count('no_bdn'))

    labels_bdn = []
    data_bdn = []
    for i in bdn:
        labels_bdn.append(i['month'].strftime("%B"))
        data_bdn.append(i['total'])

    data = {
        'skep_list': skep_list,
        'bmn_list': bmn_list,
        'bdn_total': bdn_total,
        'bmn_total': bmn_total,
        'index': True,
        'labels_bmn': labels_bmn,
        'data_bmn': data_bmn,
        'labels_bdn': labels_bdn,
        'data_bdn': data_bdn,
        'bbbmn': bbbmn,

    }
    return render(request, 'kep/index.html', data)

# Page for Web Login


def web_login(request):
    if request.method == 'GET':
        return render(request, 'kep/login.html')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'kep/login.html')

# Page to logout


def web_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


# Function for export file to CSV based on BDN


@ login_required(login_url='login')
def export_csv_bdn(request):
    if request.method == 'POST':
        tgl_awal = request.POST['tgl_awal']
        tgl_akhir = request.POST['tgl_akhir']

        response = HttpResponse(content_type='text/csv')
        writer = csv.writer(response)
        writer.writerow(['nomor_skep_sbp',
                         'tanggal_sbp',
                         'nomor_skep_bdn',
                         'tanggal_bdn',
                         'nomor_skep_bmn',
                         'tanggal_bmn',
                         'jenis_barang',
                         'merek',
                         'isi',
                         'isi_satuan',
                         'jumlah_kemasan',
                         'jumlah_kemasan_satuan',
                         'harga_jual_eceran',
                         'nilai'])

        for skep in Barang.objects.filter(nomor_skep__tanggal_bdn__range=[tgl_awal, tgl_akhir]).values_list('nomor_skep__no_sbp',
                                                                                                            'nomor_skep__tanggal_sbp',
                                                                                                            'nomor_skep__no_bdn',
                                                                                                            'nomor_skep__tanggal_bdn',
                                                                                                            'nomor_skep__no_bmn',
                                                                                                            'nomor_skep__tanggal_bmn',
                                                                                                            'jenis_barang__jenis_barang',
                                                                                                            'merek',
                                                                                                            'isi',
                                                                                                            'jenis_barang__isi_satuan',
                                                                                                            'jumlah_kemasan',
                                                                                                            'jenis_barang__jumlah_kemasan_satuan',
                                                                                                            'harga_jual_eceran',
                                                                                                            'nilai'):
            writer.writerow(skep)

        response['Content-Dispotition'] = 'attachment; filename="skep.csv"'

        return response

# Function for export file to CSV based on BMN


@ login_required(login_url='login')
def export_csv_bmn(request):
    if request.method == 'POST':
        tgl_awal = request.POST['tgl_awal']
        tgl_akhir = request.POST['tgl_akhir']

        response = HttpResponse(content_type='text/csv')
        writer = csv.writer(response)
        writer.writerow(['nomor_skep_sbp',
                         'tanggal_sbp',
                         'nomor_skep_bdn',
                         'tanggal_bdn',
                         'nomor_skep_bmn',
                         'tanggal_bmn',
                         'jenis_barang',
                         'merek',
                         'isi',
                         'isi_satuan',
                         'jumlah_kemasan',
                         'jumlah_kemasan_satuan',
                         'harga_jual_eceran',
                         'nilai'])

        for skep in Barang.objects.filter(nomor_skep__tanggal_bmn__range=[tgl_awal, tgl_akhir]).values_list('nomor_skep__no_sbp',
                                                                                                            'nomor_skep__tanggal_sbp',
                                                                                                            'nomor_skep__no_bdn',
                                                                                                            'nomor_skep__tanggal_bdn',
                                                                                                            'nomor_skep__no_bmn',
                                                                                                            'nomor_skep__tanggal_bmn',
                                                                                                            'jenis_barang__jenis_barang',
                                                                                                            'merek',
                                                                                                            'isi',
                                                                                                            'jenis_barang__isi_satuan',
                                                                                                            'jumlah_kemasan',
                                                                                                            'jenis_barang__jumlah_kemasan_satuan',
                                                                                                            'harga_jual_eceran',
                                                                                                            'nilai'):
            writer.writerow(skep)

        response['Content-Dispotition'] = 'attachment; filename="skep.csv"'

        return response
