from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login as d_login
from django.utils.translation import ugettext as _
from models import *


def index(req):
    if not req.user.is_authenticated():
        return HttpResponseRedirect('/')

    messages = Message.objects.filter(author__classroom=req.user.student.classroom).order_by('datetime').reverse()

    return render(req, 'forum/index.html', {
        'message_list': messages,
    })


def message(req, id):
    if not req.user.is_authenticated():
        return HttpResponseRedirect('/')

    message_item = get_object_or_404(Message.objects.filter(author__classroom=req.user.student.classroom, id=id))

    return render(req, 'forum/message.html', {
        'message': message_item,
    })