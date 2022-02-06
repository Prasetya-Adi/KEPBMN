from django import forms
from django.db import models
from django.forms import fields
from .models import NomorSkep, JenisBarang, Barang


class NomorSkepBdnForms(forms.Form):
    no_sbp = forms.CharField()
    tanggal_sbp = forms.DateField()
    no_bdn = forms.CharField()
    tanggal_bdn = forms.DateField()


class NomorSkepBmnForms(forms.Form):
    no_bmn = forms.CharField()
    tanggal_bmn = forms.DateField()


class TambahBarangForms(forms.ModelForm):
    class Meta:
        model = Barang
        exclude = ('nomor_skep',)


class NomorSkepForm(forms.ModelForm):
    class Meta:
        model = NomorSkep
        fields = ['no_sbp', 'tanggal_sbp', 'no_bdn', 'tanggal_bdn']
        labels = {
            'no_sbp': 'Nomor SBP',
            'tanggal_sbp': 'Tanggal SBP',
            'no_bdn': 'Nomor BDN',
            'tanggal_bdn': 'Tanggal BDN',
        }
        widgets = {
            'no_sbp': forms.TextInput(attrs={'placeholder': 'Isi Nomor SBP tanpa kode kantor. Contoh: 123, 456'}),
            'no_bdn': forms.TextInput(attrs={'placeholder': 'Isi Nomor BDN tanpa kode kantor. Contoh: 123, 456'}),
            'tanggal_sbp': forms.DateInput(attrs={'type': 'date'}),
            'tanggal_bdn': forms.DateInput(attrs={'type': 'date'}),
        }


class JenisBarangForms(forms.ModelForm):
    class Meta:
        model = JenisBarang
        fields = ['jenis_barang', 'isi_satuan', 'jumlah_kemasan_satuan']
        labels = {
            'jenis_barang': 'Jenis Barang',
            'isi_satuan': 'Satuan Isi',
            'jumlah_kemasan_satuan': 'Satuan Jumlah Kemasan'

        }
