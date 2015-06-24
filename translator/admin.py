from django.contrib import admin


# Register your models here.
from translator.models import *

admin.site.register(Scenario)
admin.site.register(Step)
admin.site.register(AtomicActionComponent)
admin.site.register(UserActionComponent)