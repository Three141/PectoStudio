from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from main.models import Student, ProgramFile, Class


class StudentInline(admin.TabularInline):
    model = Student


class StudentAdmin(UserAdmin):
    inlines = [
        StudentInline,
    ]


class FileAdmin(admin.ModelAdmin):
    list_filter = ('owner',)


admin.site.unregister(User)
admin.site.register(User, StudentAdmin)
admin.site.register(Student)
admin.site.register(ProgramFile, FileAdmin)
admin.site.register(Class)
