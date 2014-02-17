from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User, verbose_name=_("Base user"), )
    classroom = models.ForeignKey('Class', verbose_name=_("Class"))

    def __unicode__(self):
        return self.user.get_username() + " | " + self.user.get_full_name()

    def get_student_files(self):
        my_files = ProgramFile.objects.filter(owner=self)
        my_files_names = []
        for f in my_files:
            my_files_names.append(unicode(f))
        return my_files_names

    def get_shared_with_student(self):
        #shared_with_me = ProgramFile.objects.filter(owner__classroom=self.classroom, shared_with_class=True)
        classmates = Student.objects.filter(classroom=self.classroom)
        shared_with_me_names = {}
        for mate in classmates:
            shared_with_me = ProgramFile.objects.filter(owner=mate, shared_with_class=True)
            if not shared_with_me or mate == self:
                continue
            shared_with_me_names[unicode(mate)] = []
            for file in shared_with_me:
                shared_with_me_names[unicode(mate)].append(unicode(file))
        return shared_with_me_names

    class Meta:
        verbose_name = _('Student')
        verbose_name_plural = _('Students')


class ProgramFile(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=30, default="no_name")
    data = models.TextField(verbose_name=_("Data"), blank=True)
    owner = models.ForeignKey(Student, verbose_name=_("Owner"))
    shared_with_class = models.BooleanField(verbose_name=_("Shared with class"), default=False)

    def __unicode__(self):
        return self.name

    def get_data(self):
        return self.data

    class Meta:
        verbose_name = _('file')
        verbose_name_plural = _('files')


class Class(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=20)
    teachers = models.ManyToManyField(User, verbose_name=_("Teachers"), related_name="teacher_of")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('class')
        verbose_name_plural = _('classes')