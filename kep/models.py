from django.db import models
from django.db.models.deletion import CASCADE
from datetime import date


class NomorSkep(models.Model):
    no_sbp = models.CharField(max_length=100, unique=True)
    tanggal_sbp = models.DateField(blank=True, null=True)
    no_bdn = models.CharField(max_length=100, unique=True)
    tanggal_bdn = models.DateField()
    no_bmn = models.CharField(
        max_length=100, blank=True, null=True, unique=True)
    tanggal_bmn = models.DateField(blank=True, null=True)

    def __str__(self):
        no = "SBP:"+self.no_sbp+", BDN:"+self.no_bdn+", BMN:"+self.no_bmn
        return no

    def no_bdn_full(self):
        tahun = self.tanggal_bdn.year
        no = "KEP-"+self.no_bdn+"/WBC.09/KPP.MP.06/"+str(tahun)
        return no

    def no_bmn_full(self):
        tahun = self.tanggal_bmn.year
        no = "KEP-"+self.no_bmn+"/WBC.09/KPP.MP.06/"+str(tahun)
        return no

    def jumlah_barang(self):
        total = Barang.objects.filter(nomor_skep=self).count()
        return total


class JenisBarang(models.Model):
    jenis_barang = models.CharField(max_length=100)
    isi_satuan = models.CharField(max_length=100)
    jumlah_kemasan_satuan = models.CharField(max_length=100)

    def __str__(self):
        jenis = self.jenis_barang+", satuan: "+self.isi_satuan + \
            ", kemasan: "+self.jumlah_kemasan_satuan
        return jenis


class Barang(models.Model):
    nomor_skep = models.ForeignKey(NomorSkep, on_delete=CASCADE)
    jenis_barang = models.ForeignKey(JenisBarang, on_delete=CASCADE)
    merek = models.CharField(max_length=100)
    isi = models.IntegerField()
    jumlah_kemasan = models.IntegerField()
    harga_jual_eceran = models.IntegerField()
    nilai = models.IntegerField()

    def __str__(self):
        return self.merek

    def total_satuan(self):
        total = self.isi * self.jumlah_kemasan
        return total
