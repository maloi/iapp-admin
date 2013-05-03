from django.http import HttpResponse
from django.shortcuts import render

from lib.group import Group
from lib.user import User

def index(request):
    all_group = Group.all(['cn', ])
    context = {'all_group' : all_group,}
    return render(request, 'iapp_group/index.html', context)

def group(request, cn):
    groups = Group.get_by_cn(cn, ['cn', 'gidNumber', 'memberUid'])
    users = User.all(['uid', 'cn'])
    context = {'groups' : groups,
                    'users' : users,
                    }
    return render(request, 'iapp_group/index.html', context)