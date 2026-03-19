from django.contrib import admin
from .models import Subject, StandardSubject, Assignment, Submission, Standard, TeacherStandard

# Register your models here.
admin.site.register(Subject)
admin.site.register(StandardSubject)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Standard)
admin.site.register(TeacherStandard)