# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin

# Create your models here.
class App(models.Model):
    CHOICES = (
        ("0", "明文"),
        ("1", "密文"),
    )
    name = models.CharField("名称", max_length=16, default="")
    app_id = models.IntegerField("客户ID", primary_key=True, default=0)
    app_key = models.CharField("Key", max_length=32, default="")
    app_secret = models.CharField("Secret", max_length=32, default="")
    is_encrypt = models.CharField("是否加密", choices=CHOICES, default="0", max_length=2)
    remark1 = models.TextField("公钥", max_length=1024, default="")
    remark2 = models.TextField("私钥", max_length=1024, default="")


class AppAdmin(admin.ModelAdmin):
    list_display=('app_id', 'name', 'app_key', 'app_secret', 'is_encrypt')
    search_fields=('name',)    
    list_filter = ('is_encrypt',)                 
    ordering = ('app_id','name')
    #fields = ('app_id', 'name', 'app_key', 'app_secret', 'is_encrypt', 'remark1', 'remake2')

    fieldsets = (
        ('Base Info', {'fields': ('app_id', 'name')}),
        ('Meta Data', {'fields': ('app_key', 'app_secret', 'is_encrypt', 'remark1', 'remark2')}),
    )

class Service(models.Model):
    name = models.CharField(max_length=16, default="")
    url = models.CharField(max_length=64, default="")
    text = models.CharField(max_length=128, default="")


class ServiceAdmin(admin.ModelAdmin):
    list_display=('name', 'url', 'text')
    search_fields=('name',)    
    list_filter = ('name',)                 
    ordering = ('name','url')
    fields = ('name', 'url', 'text')


class Request_limit(models.Model):
    app = models.ForeignKey('App', verbose_name="list of apps")
    service = models.ForeignKey('Service', verbose_name="list of services")
    limit_value = models.IntegerField(default=0)

class RequestlimitAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display=('app', 'service', 'limit_value')
    search_fields=('app','service')    
    list_filter = ('limit_value',)                 
    ordering = ('app','service')
    fields = ('app', 'service', 'limit_value')


admin.site.register(App, AppAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Request_limit, RequestlimitAdmin)

