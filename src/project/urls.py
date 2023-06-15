from django.contrib import admin
from django.urls import path,include
from django.conf import settings as st
from django.conf.urls.static import static as sc
import django

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',include('skin.urls',namespace='skin')),
    
    path('i18n/',include('django.conf.urls.i18n')),
]
if st.DEBUG:
    urlpatterns += sc(st.STATIC_URL,document_root=st.STATIC_ROOT)
    urlpatterns += sc(st.MEDIA_URL,document_root=st.MEDIA_ROOT)

