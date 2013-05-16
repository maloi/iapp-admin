from django.shortcuts import render

from lib.user import User

def index(request):
    users = User.all(['cn','uid', 'uidNumber'])
    context = {'users': users}
    return render(request, 'iapp_user/index.html', context)

def detail(request, uid):
    user = User.get_by_uid(uid)
    import pprint; pprint.pprint(user.all_fields)
    context = {'user': user}
    return render(request, 'iapp_user/detail.html', context)

def edit(request, uid=None):
    if uid == None:
        user = User()
    else:
        user = User.get_by_uid(uid)
    context = {'user': user}
    return render(request, 'iapp_user/edit.html', context)
