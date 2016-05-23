# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin

# Create your models here.
class App(models.Model):
    CHOICES = (
        ("0", "明文"),
        ("1", "密文"),
    )
    name = models.CharField("name", max_length=32, default="")
    app_id = models.CharField("app_id", primary_key=True, max_length=16, default="")
    app_key = models.CharField("Key", max_length=32, default="")
    app_secret = models.CharField("Secret", max_length=32, default="")
    is_encrypt = models.CharField("is_encrypt", choices=CHOICES, default="0", max_length=2)
    remark1 = models.TextField("remark1", max_length=1024, default="")
    remark2 = models.TextField("remark2", max_length=1024, default="")
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'App'
        verbose_name_plural = 'App'
   
    def __unicode__(self):
        return self.name


class AppAdmin(admin.ModelAdmin):
    list_display=('app_id', 'name', 'app_key', 'app_secret', 'is_encrypt', 'update_time')
    search_fields=('name',)    
    list_filter = ('is_encrypt',)                 
    ordering = ('app_id','name')
    readonly_fields = ('update_time',)
    #fields = ('app_id', 'name', 'app_key', 'app_secret', 'is_encrypt', 'remark1', 'remake2')

    fieldsets = (
        ('Base Info', {'fields': ('app_id', 'name')}),
        ('Meta Data', {'fields': ('app_key', 'app_secret', 'is_encrypt', 'remark1', 'remark2')}),
    )

class Service(models.Model):
    name = models.CharField("name", max_length=16, default="")
    url = models.CharField("url", max_length=64, default="")
    text = models.TextField("text", max_length=128, default="")
    update_time = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Service'
   
    def __unicode__(self):
        return self.name

class SuccessRatio(models.Model):
    request_time = models.DateTimeField(auto_now=True, verbose_name=u'时间')
    service = models.ForeignKey('Service', verbose_name="services", unique=False)
    biz_success = models.IntegerField(verbose_name=u'成功率')
    biz_fail = models.IntegerField(verbose_name=u'失败率')
    unique_together = (("request_time", "service"),)

class ServiceAdmin(admin.ModelAdmin):
    list_display=('name', 'url', 'text', 'update_time')
    search_fields=('name', 'url')    
    ordering = ('name','url')
    fields = ('name', 'url', 'text')
    readonly_fields = ('update_time',)

class Requestlimit(models.Model):
    app = models.ForeignKey('App', verbose_name="list of apps")
    service = models.ForeignKey('Service', verbose_name="list of services")
    limit_value = models.IntegerField(default=0)
    update_time = models.DateTimeField(auto_now=True)

class RequestlimitAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display=('app', 'service', 'limit_value', 'update_time')
    search_fields=('app','service')    
    list_filter = ('limit_value',)                 
    ordering = ('app','service')
    fields = ('app', 'service', 'limit_value')
    readonly_fields = ('update_time',)

class SuccessRatioAdmin(admin.ModelAdmin):
    list_display=('request_time', 'service', 'biz_success', 'biz_fail')
    ordering = ('request_time', 'service')
    readonly_fields=('request_time', 'service', 'biz_success', 'biz_fail')
    search_fields=('service',)    
    list_filter = ('request_time',)                 
   
    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


admin.site.register(App, AppAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Requestlimit, RequestlimitAdmin)
admin.site.register(SuccessRatio, SuccessRatioAdmin)

