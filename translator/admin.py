from django.contrib import admin


# Register your models here.
from translator.models import RobotProgram, ProgramStep

admin.site.register(RobotProgram)
admin.site.register(ProgramStep)