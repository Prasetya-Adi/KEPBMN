
from django.urls import path

from .views import views
from kep.views.views_bdn import bdn_update, bdn_delete, bdn_detail, list_bdn
from kep.views.views_bmn import list_bmn, detail_bmn
from kep.views.views_barang import tambah_barang_bdn, update_barang_bdn, barang_delete
from kep.views.views_jenis_barang import jenisbarang, jenisbarang_delete, jenisbarang_update

urlpatterns = [
    # LOGIN and LOGOUT
    path('', views.web_login, name="login"),
    path('login', views.web_login, name="login"),
    path('logout', views.web_logout, name='logout'),

    # INDEX and Function Export CSV
    path('index', views.index, name="index"),
    path('download/bmn', views.export_csv_bmn, name="export-csv-bmn"),
    path('download/bdn', views.export_csv_bdn, name="export-csv-bdn"),

    # BDN
    path('bdn/list', list_bdn, name='list-bdn'),
    path('bdn/update/<id>', bdn_update, name='update-bdn'),
    path('bdn/delete/<id>', bdn_delete, name='delete-bdn'),
    path('bdn/detail/<id>', bdn_detail, name='detail-bdn'),

    # BARANG
    path('barang/tambah-barang/<id>', tambah_barang_bdn,
         name='tambah-barang-bdn'),
    path('barang/update-barang/<id>', update_barang_bdn,
         name='update-barang-bdn'),
    path('barang/delete-barang/<id>', barang_delete,
         name='delete-barang-bdn'),

    # BMN
    path('list-bmn', list_bmn, name='list-bmn'),
    path('detail-bmn/<id>', detail_bmn, name='detail-bmn'),

    # JENIS BARANG
    path('jenis-barang/list', jenisbarang, name='jenis-barang-list'),
    path('jenis-barang/update/<id>', jenisbarang_update, name='update-jb'),
    path('jenis-barang/delete/<id>', jenisbarang_delete, name='delete-jb'),


    # coba
    #path('coba', views.coba, name='coba')
]
