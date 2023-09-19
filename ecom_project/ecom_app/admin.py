from django.contrib import admin
from.models import Category,products
# Register your models here.

class categoryadmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields = {'slug':('name',)}
admin.site.register(Category,categoryadmin)

class productadmin(admin.ModelAdmin):
    list_display = ['name','stock','prize','available','created','updated']
    list_editable = ['prize','stock','available']
    prepopulated_fields = {'slug':('name','prize')}
admin.site.register(products,productadmin)
