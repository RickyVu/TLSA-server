from django.contrib import admin
from .models import Class, ClassLocation, TeachClass, ClassComment, Experiment, ExperimentImage, ExperimentFile

# Register your models here.
admin.site.register(Class)
admin.site.register(ClassLocation)
admin.site.register(TeachClass)
admin.site.register(ClassComment)
admin.site.register(Experiment)
admin.site.register(ExperimentImage)
admin.site.register(ExperimentFile)