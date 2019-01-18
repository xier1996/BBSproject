"""BBSproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from my_web import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',views.index),
    url(r'^detail/(\d+)/(\d+)$',views.bbs_detail,name='show_comment'),
    url(r'^sub_comment/$',views.sub_comment),
    url(r'^login/$',views.login),
    url(r'^acc_login/$',views.acc_login),
    url(r'^logout/$', views.logout_view),
    url(r'^bbs_pub/$',views.bbs_pub),
    url(r'^bbs_sub/(\d+)/$',views.bbs_sub),
    url(r'^category/(\d+)/(\d+)/$',views.category,name='show_bbs'),
    url(r'^register/$',views.register),
    url(r'^acc_reg/$', views.acc_reg),
    url(r'^accounts_profile/$',views.accounts_profile),
    url(r'^updatepassword/$',views.updatepassword),
    url(r'^edit_bbs_detail/$',views.edit_bbs_detail),
    url(r'^update_bbs_detail/$',views.update_bbs_detail),
    url(r'^userinfo/(\d+)/$',views.userinfo),
    url(r'^search/$',views.search_bbs),
    url(r'^search_res/(\d+)/$',views.search_res,name='show_res')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
