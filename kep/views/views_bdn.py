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
from ..forms import NomorSkepBmnForms, NomorSkepForm

from ..engine_to_django import make_bdn_2

import io
import csv


@login_required(login_url='login')
# Create skep BDN and List
def list_bdn(request):
    # get all skep list
    skep_list = NomorSkep.objects.all().order_by('-no_bdn')
    form = NomorSkepForm(request.POST or None)

    # get the list of skep BDN with paginator 5 per page
    if request.method == 'GET':
        paginator = Paginator(skep_list, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'skep_list': skep_list,
                   'form': form,
                   'page_obj': page_obj,
                   'menu_bdn': True}
        return render(request, 'kep/bdn/list.html', context)

    # post the new bdn skep
    if request.method == 'POST':
        action = request.POST['action']
        if (action == 'addBDN'):
            if form.is_valid():
                form.save()
            return HttpResponseRedirect(reverse('list-bdn'))


@user_passes_test(checkP2)
# To Update skep bdn
def bdn_update(request, id):
    bdn = get_object_or_404(NomorSkep, id=id)
    form = NomorSkepForm(request.POST or None, instance=bdn)
    context = {'form': form, 'menu_bdn': True}

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('list-bdn'))

    return render(request, "kep/bdn/update.html", context)


@user_passes_test(checkP2)
# To Delete skep bdn
def bdn_delete(request, id):
    skep = get_object_or_404(NomorSkep, id=id)
    if request.method == 'POST':
        skep.delete()
        return HttpResponseRedirect(reverse('list-bdn'))
    return render(request, "kep/bdn/delete.html")


# @user_passes_test(checkP2)
# Detail and Download Skep BDN
def bdn_detail(request, id):
    bdn = get_object_or_404(NomorSkep, id=id)
    barang = Barang.objects.filter(nomor_skep=id)
    context = {'bdn': bdn, 'barang': barang, 'menu_bdn': True}
    id_skep = id

    # Detail Skep BDN
    if request.method == 'GET':
        return render(request, 'kep/bdn/detail.html', context)

    elif request.method == 'POST':
        # instantiate all unique forms (using prefix) as unbound
        skep_bmn = NomorSkepBmnForms(prefix='bmn')

        # determine which form is submitting (based on hidden input called 'action')
        action = request.POST['action']
        bdn_id = request.POST['id']

        # MENGUBAH STATUS BDN MENJADI BMN
        if (action == 'jadikan_bmn'):
            skep_bmn = NomorSkepBmnForms(request.POST, prefix='bmn')
            if skep_bmn.is_valid():
                no_bmn = skep_bmn.cleaned_data['no_bmn']
                tanggal_bmn = skep_bmn.cleaned_data['tanggal_bmn']
                bmn = NomorSkep.objects.get(id=bdn_id)
                bmn.no_bmn = no_bmn
                bmn.tanggal_bmn = tanggal_bmn
                bmn.save()
            return HttpResponseRedirect(reverse('list-bmn'))

        # MENDOWNLOAD FILE SKEP BDN
        elif (action == 'download'):
            no_kep_bdn = bdn.no_bdn
            tgl_kep_bdn = bdn.tanggal_bdn
            no_sbp = bdn.no_sbp
            tgl_sbp = bdn.tanggal_sbp
            chr(47)
            no_kep_bdn_full = "KEP_" + \
                str(no_kep_bdn)+chr(47)+"WBC.09/KPP.MP.06/" + \
                tgl_kep_bdn.strftime('%Y')

            # Make Doc with engine python-docx
            document = make_bdn_2(id_skep, no_kep_bdn,
                                  tgl_kep_bdn, no_sbp, tgl_sbp)

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
                no_kep_bdn_full+'.docx'
            response["Content-Encoding"] = 'UTF-8'
            return response
