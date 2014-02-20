from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login as d_login
from forms import *
from models import *
from string import replace


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

    if req.method == 'POST':
        form = NewCommentForm(req.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['data'] = replace(data['data'], "\n", "<br>")
            comm = Comment(data=data['data'], author=req.user.student, on=message_item)
            comm.save()

    return render(req, 'forum/message.html', {
        'message': message_item,
    })


def new_message(req):
    if not req.user.is_authenticated():
        return HttpResponseRedirect('/')

    if req.method == 'POST':
        form = NewPostForm(req.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['data'] = replace(data['data'], "\n", "<br>")
            post = Message(title=data['title'], data=data['data'], author=req.user.student)
            post.save()
            return HttpResponseRedirect('/forum/message/'+str(post.id)+'/')

    return render(req, 'forum/newpost.html')