from django.http import HttpResponse
from django.shortcuts import render
from operator import  attrgetter

from lib.group import Group
from lib.user import User

def index(request):
    all_group = Group.all(['cn', ])
    context = {'all_group' : all_group,}
    return render(request, 'iapp_group/index.html', context)

def group(request, cn):
    groups = Group.get_by_cn(cn, ['cn', 'gidNumber', 'memberUid'])
    users = User.all(['uid', 'cn', 'givenName', 'sn'])
    sort_users = sorted(users, key=attrgetter('sn'))
    context = {'groups' : groups,
                    'users' : sort_users,
                    }
    return render(request, 'iapp_group/index.html', context)