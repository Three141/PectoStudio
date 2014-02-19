from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as d_login, logout as d_logout
from django.utils.translation import ugettext as _
from forms import *
from models import ProgramFile, Student
import json


def index(req):
    if req.user.is_authenticated():
        return home_logon(req)
    is_bad_login = False
    if req.method == 'POST':
        form = LoginForm(req.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user is not None:
                d_login(req, user)
                return home_logon(req)
            else:
                is_bad_login = True
        else:
            is_bad_login = True
    else:
        form = LoginForm()

    return render(req, 'login.html', {
        'form': form,
        'bad_login': is_bad_login,
    })


def home_logon(req):
    return render(req, 'main.html', {
    })


def nfc_login(req):
    if req.user.is_authenticated():
        return home_logon(req)
    user = authenticate(username=req.GET['username'], password=req.GET['password'])
    if user is not None:
        d_login(req, user)
    return HttpResponseRedirect("/")


def logout(req):
    d_logout(req)
    return HttpResponseRedirect("/")


def get_all_files(req):
    if not req.user.is_authenticated():
        return HttpResponse(json.dumps({'success': False, 'error_msg': _('Not connected')}), content_type="application/json")
    my_files_names = req.user.student.get_student_files()
    shared_with_me_names = req.user.student.get_shared_with_student()
    response_data = {
        "my_files": my_files_names,
        "shared_with_me": shared_with_me_names,
        'success': True
    }
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def get_file_data_by_name(req, file_name):
    if not req.user.is_authenticated():
        return HttpResponse(json.dumps({'success': False, 'error_msg': _('Not connected')}), content_type="application/json")
    pfile = ProgramFile.objects.filter(owner=req.user.student, name=file_name)
    if not pfile:
        return HttpResponse(json.dumps({'success': False, 'error_msg': _('File not found')}), content_type="application/json")
    pfile = pfile[0]
    response_data = {
        'name': unicode(pfile),
        'data': pfile.get_data(),
        'shared': pfile.shared_with_class,
        'success': True
    }
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def get_shared_file_data_by_name(req, file_owner, file_name):
    if not req.user.is_authenticated():
        return HttpResponse(json.dumps({'success': False, 'error_msg': _('Not connected')}), content_type="application/json")
    owner_student = Student.objects.filter(user__username=file_owner)
    if not owner_student:
        return HttpResponse(json.dumps({'success': False, 'error_msg': _('Unknown student')}), content_type="application/json")
    owner_student = owner_student[0]
    pfile = ProgramFile.objects.filter(owner=owner_student, name=file_name, shared_with_class=True)
    if not pfile:
        return HttpResponse(json.dumps({'success': False, 'error_msg': _('File not found')}), content_type="application/json")
    pfile = pfile[0]
    response_data = {
        'name': unicode(pfile),
        'data': pfile.get_data(),
        'shared': pfile.shared_with_class,
        'success': True
    }
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def save_file_by_name(req, file_name):
    if not req.user.is_authenticated():
        return HttpResponse(json.dumps({'success': False, 'error_msg': _('Not connected')}), content_type="application/json")
    if req.method != 'POST':
        return HttpResponse(json.dumps({'success': False, 'error_msg': _('Not a POST request')}), content_type="application/json")
    pfile = ProgramFile.objects.filter(owner=req.user.student, name=file_name)
    if not pfile:
        return HttpResponse(json.dumps({'success': False, 'error_msg': _('File not found')}), content_type="application/json")
    for file in pfile:
        if file.owner == req.user.student:
            pfile = pfile[0]
            pfile.data = req.POST['data']
            pfile.save()
            return HttpResponse(json.dumps({'success': True}), content_type="application/json")
    return HttpResponse(json.dumps({'success': False, 'error_msg': _('You\'re not allowed to perform this action')}), content_type="application/json")


def share_file_by_name(req, file_name):
    if not req.user.is_authenticated():
        return HttpResponse(json.dumps({'success': False, 'error_msg': _('Not connected')}), content_type="application/json")
    pfile = ProgramFile.objects.filter(owner=req.user.student, name=file_name)
    if not pfile:
        return HttpResponse(json.dumps({'success': False, 'error_msg': _('File not found')}), content_type="application/json")
    for file in pfile:
        if file.owner == req.user.student:
            pfile = pfile[0]
            pfile.shared_with_class = not pfile.shared_with_class
            pfile.save()
            outmsg = ''
            if pfile.shared_with_class:
                outmsg = _('The file has been shared!')
            else:
                outmsg = _('The file has been unshared!')
            return HttpResponse(json.dumps({'message': outmsg, 'success': True}), content_type="application/json")
    return HttpResponse(json.dumps({'success': False, 'error_msg': _('You\'re not allowed to perform this action')}), content_type="application/json")


def new_file(req, file_name):
    if not req.user.is_authenticated():
        return HttpResponse(json.dumps({'success': False, 'error_msg': _('Not connected')}), content_type="application/json")
    if ProgramFile.objects.filter(name=file_name, owner=req.user):
        return HttpResponse(json.dumps({'success': False, 'error_msg': _('File with that name already exists')}), content_type="application/json")
    pfile = ProgramFile(name=file_name, owner=req.user.student)
    pfile.save()
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


def delete_file(req, file_name):
    if not req.user.is_authenticated():
        return HttpResponse(json.dumps({'success': False, 'error_msg': _('Not connected')}), content_type="application/json")
    pfile = ProgramFile.objects.filter(name=file_name)
    if not pfile:
        return HttpResponse(json.dumps({'success': False, 'error_msg': _('File not found')}), content_type="application/json")
    for file in pfile:
        if file.owner == req.user.student:
            pfile.delete()
            return HttpResponse(json.dumps({'success': True}), content_type="application/json")
    return HttpResponse(json.dumps({'success': False, 'error_msg': _('You\'re not allowed to do it')}), content_type="application/json")