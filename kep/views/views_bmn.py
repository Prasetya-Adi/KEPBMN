import imp
from django.http.response import StreamingHttpResponse
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test, login_required
from .views_decorator import checkPabean, checkP2

from ..models import NomorSkep, Barang
from ..engine_to_django import make_bmn_2
import io
import csv


@login_required(login_url='login')
def list_bmn(request):
    skep_list = NomorSkep.objects.all().filter(
        no_bmn__isnull=False).order_by('-no_bmn')
    if request.method == 'GET':
        paginator = Paginator(skep_list, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'skep_list': skep_list,
                   'page_obj': page_obj,
                   'menu_bmn': True}
        return render(request, 'kep/bmn/list.html', context)

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
                         'harga_jual_eceran_satuan',
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
                                                                                                            'isi_satuan__satuan',
                                                                                                            'jumlah_kemasan',
                                                                                                            'jumlah_kemasan_satuan__satuan',
                                                                                                            'harga_jual_eceran',
                                                                                                            'harga_jual_eceran_satuan__satuan',
                                                                                                            'nilai'):
            writer.writerow(skep)

        response['Content-Dispotition'] = 'attachment; filename="skep.csv"'

        return response


@user_passes_test(checkPabean)
def detail_bmn(request, id):
    bmn = get_object_or_404(NomorSkep, id=id)
    barang = Barang.objects.filter(nomor_skep=id)
    data = {'bmn': bmn, 'barang': barang, 'menu_bmn': True}

    if request.method == 'GET':
        print(bmn.no_bmn_full())
        return render(request, 'kep/bmn/detail.html', data)

    # MENDOWNLOAD FILE BMN
    elif request.method == 'POST':

        action = request.POST['action']
        bmn_id = request.POST['id']

        if (action == 'jadikan_bdn'):
            bmn = NomorSkep.objects.get(id=bmn_id)
            bmn.no_bmn = None
            bmn.tanggal_bmn = None
            bmn.save()
            return HttpResponseRedirect(reverse('list-bmn'))

         # MENDOWNLOAD FILE SKEP BDN
        elif (action == 'download'):
            no_kep_bmn = bmn.no_bmn
            tgl_kep_bmn = bmn.tanggal_bmn
            no_kep_bdn = bmn.no_bdn
            tgl_kep_bdn = bmn.tanggal_bdn
            id_skep = id
            no_kep_bmn_full = "KEP_" + \
                str(no_kep_bmn)+chr(47)+"WBC.09/KPP.MP.06/" + \
                tgl_kep_bdn.strftime('%Y')

            # Edit Doc
            document = make_bmn_2(id_skep, no_kep_bmn,
                                  tgl_kep_bmn, no_kep_bdn, tgl_kep_bdn)

            # Save document info
            buffer = io.BytesIO()
            document.save(buffer)  # save your memory stream
            buffer.seek(0)  # rewind the stream

            # put them to streaming content response
            # within docx content_type
            response = StreamingHttpResponse(
                streaming_content=buffer,  # use the stream's content
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )

            response['Content-Disposition'] = 'attachment;filename=' + \
                no_kep_bmn_full+'.docx'
            response["Content-Encoding"] = 'UTF-8'
            return response

    return render(request, 'kep/bmn/detail.html', data)
