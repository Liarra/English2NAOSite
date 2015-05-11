from django.contrib import admin


# Register your models here.
from translator.models import *

admin.site.register(RobotProgram)
admin.site.register(ProgramStep)
admin.site.register(AtomicActionComponent)
admin.site.register(UserActionComponent)