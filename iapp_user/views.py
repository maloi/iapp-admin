from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from lib.user import User

@login_required
def index(request):
    users = User.all(['cn','uid', 'uidNumber'])
    context = {'users': users}
    return render(request, 'iapp_user/index.html', context)

@login_required
def details(request, uid):
    iapp_user = User.get_by_uid(uid)
    context = {'iapp_user': iapp_user,
              }
    return render(request, 'iapp_user/details.html', context)

@login_required
def edit(request, uid=None):
    if uid == None:
        iapp_user = User()
    else:
        iapp_user = User.get_by_uid(uid)
    context = {'iapp_user': iapp_user}
    return render(request, 'iapp_user/edit.html', context)
