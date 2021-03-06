from django.contrib import admin


# Register your models here.
from translator.models import *


class ComponentAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'summary')


admin.site.register(Scenario)
admin.site.register(Step)
admin.site.register(AtomicActionComponent,ComponentAdmin)
admin.site.register(AtomicConditionComponent, ComponentAdmin)
admin.site.register(UserActionComponent)