from django.contrib import admin
from firstapp.models import Wear
from firstapp.models import Cart

# Register your models here.
#admin.site.register(Student)

class WearAdmin(admin.ModelAdmin):
    list_display=['id','name','category','price']
    list_filter=['category']


class CartAdmin(admin.ModelAdmin):
    list_display=['id','sid','uid','quantity']


admin.site.register(Wear,WearAdmin)
admin.site.register(Cart,CartAdmin)

# Register your models here.
