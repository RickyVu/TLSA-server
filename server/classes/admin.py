from django.contrib import admin
from .models import Class, ClassLocation, TeachClass, ClassComment

# Register your models here.
admin.site.register(Class)
admin.site.register(ClassLocation)
admin.site.register(TeachClass)
admin.site.register(ClassComment)