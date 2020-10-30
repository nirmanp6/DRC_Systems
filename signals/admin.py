from django.contrib import admin

from .models import ProductSignal, UserSignal
# Register your models here.
class SignalAdmin(admin.ModelAdmin):
    readonly_fields = ('at',)


admin.site.register(ProductSignal, SignalAdmin)
admin.site.register(UserSignal, SignalAdmin)