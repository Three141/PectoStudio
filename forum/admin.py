from django.contrib import admin
from models import *
from main.models import Class
from django.utils.translation import ugettext_lazy as _


class CommentInline(admin.TabularInline):
    model = Comment


class ClassListFilter(admin.SimpleListFilter):
    title = _('Class')
    parameter_name = 'classroom'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        classs = Class.objects.all()
        a = []
        for c in classs:
            a.append((unicode(c), unicode(c)))
        a = tuple(a)
        return a

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if not self.value():
            return queryset.filter()
        return queryset.filter(author__classroom__name=self.value())


class MessageAdmin(admin.ModelAdmin):
    list_filter = (ClassListFilter, 'author',)
    list_display = ('title', 'author', 'get_comments_len', 'get_class',)
    inlines = [
        CommentInline,
    ]


admin.site.register(Message, MessageAdmin)