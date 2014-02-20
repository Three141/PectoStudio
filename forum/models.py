from django.db import models
from main.models import Student
from django.utils.translation import ugettext_lazy as _


class Message(models.Model):
    title = models.CharField(max_length=50, verbose_name=_('Title'))
    author = models.ForeignKey(Student, verbose_name=_('Author'))
    datetime = models.DateTimeField(auto_now_add=True, verbose_name=_('Time'))
    data = models.TextField(verbose_name=_('Data'))

    def __unicode__(self):
        return self.title

    def get_comments(self):
        return self.comment_set.all().order_by('datetime')

    class Meta:
        verbose_name = _('message')
        verbose_name_plural = _('messages')


class Comment(models.Model):
    author = models.ForeignKey(Student, verbose_name=_('Author'))
    datetime = models.DateTimeField(auto_now_add=True, verbose_name=_('Time'))
    data = models.TextField(verbose_name=_('Data'))
    on = models.ForeignKey(Message, verbose_name=_('On'))

    def __unicode__(self):
        return self.data

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')