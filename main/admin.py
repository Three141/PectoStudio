from django.contrib import admin
from django.contrib.auth.models import User
from main.models import Student, ProgramFile, Class


class StudentInline(admin.TabularInline):
    model = Student


class UserAdmin(admin.ModelAdmin):
    inlines = [
        StudentInline,
    ]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Student)
admin.site.register(ProgramFile)
admin.site.register(Class)
