from django.db import models
from django.contrib import admin

# Create your models here.
class App(models.Model):
    app_id = models.IntegerField(primary_key=True, default=0)
    name = models.CharField(max_length=16, default="")
    app_key = models.CharField(max_length=32, default="")
    secret = models.CharField(max_length=32, default="")
    is_encrypt = models.IntegerField(default=0)
    remark1 = models.CharField(max_length=1024, default="")
    remake2 = models.CharField(max_length=1024, default="")

class AppAdmin(admin.ModelAdmin):
    list_display=('app_id', 'name', 'app_key', 'secret', 'is_encrypt', 'remark1', 'remake2')
    search_fields=('name',)    
    list_filter = ('is_encrypt',)                 
    ordering = ('app_id','name')
    fields = ('app_id', 'name', 'app_key', 'secret', 'is_encrypt', 'remark1', 'remake2')

    #fieldsets = (
    #    ('Base Info', {'fields': ('app_id', 'name')}),
    #    ('Meta Data', {'fields': ('app_key', 'secret', 'is_encrypt', 'remark1', 'remark2')}),
    #)

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
    #list_display=('app', 'service', 'limit_value')
    search_fields=('app','service')    
    #list_filter = ('app',)                 
    #ordering = ('app','service')
    #fields = ('app', 'service', 'limit_value')


admin.site.register(App, AppAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Request_limit, RequestlimitAdmin)

