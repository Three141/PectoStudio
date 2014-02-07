from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login as d_login, logout as d_logout
from forms import *
from models import ProgramFile
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
        'file_list': req.user.programfile_set.all(),
    })

def logout(req):
    d_logout(req)
    return HttpResponseRedirect("/")


def get_all_files(req):
    if not req.user.is_authenticated():
        raise Http404("Please login")
    my_files = ProgramFile.objects.filter(owner=req.user)
    my_files_names = []
    for f in my_files:
        my_files_names.append(unicode(f))
    shared_with_me = ProgramFile.objects.filter(owner__student__classroom=req.user.student.classroom, shared_with_class=True)
    shared_with_me_names = []
    for f in shared_with_me:
        shared_with_me_names.append([unicode(f.owner.student), unicode(f)])
    response_data = {
        "my_files": my_files_names,
        "shared_with_me": shared_with_me_names,
        'success': True
    }
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def get_file_data_by_name(req, file_name):
    if not req.user.is_authenticated():
        raise Http404("Please login")
    pfile = ProgramFile.objects.filter(owner=req.user, name=file_name)[0]
    if not pfile:
        return HttpResponse(json.dumps({'success': False}), content_type="application/json")
    response_data = {
        "name": unicode(pfile),
        "data": pfile.get_data(),
        'success': True
    }
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def save_file_by_name(req, file_name):
    if not req.user.is_authenticated():
        raise Http404("Please login")
    if req.method != 'POST':
        return HttpResponse(json.dumps({'success': False}), content_type="application/json")
    pfile = ProgramFile.objects.filter(owner=req.user, name=file_name)[0]
    if not pfile:
        return HttpResponse(json.dumps({'success': False}), content_type="application/json")
    pfile.data = req.POST['data']
    pfile.save()
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


def new_file(req, file_name):
    if not req.user.is_authenticated():
        raise Http404("Please login")
    pfile = ProgramFile(name=file_name, owner=req.user)
    pfile.save()
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")


def delete_file(req, file_name):
    if not req.user.is_authenticated():
        raise Http404("Please login")
    pfile = ProgramFile.objects.filter(owner=req.user, name=file_name)[0]
    if not pfile:
        return HttpResponse(json.dumps({'success': False}), content_type="application/json")
    pfile.delete()
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")