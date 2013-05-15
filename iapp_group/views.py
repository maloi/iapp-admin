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
<<<<<<< HEAD
    groups = Group.get_by_cn(cn, ['cn', 'gidNumber', 'memberUid'])
    users = User.all(['uid', 'cn', 'givenName', 'sn'])
    sort_users = sorted(users, key=attrgetter('sn'))
    context = {'groups' : groups,
                    'users' : sort_users,
                    }
    return render(request, 'iapp_group/index.html', context)
=======
    group = Group.get_by_cn(cn, ['cn', 'gidNumber', 'memberUid'])
    members = []
    for memberUid in group.memberUid:
        members.append(User.get_by_uid(memberUid, ['cn', 'uid']))
    context = {
              'group': group,
              'members': members,
              }
    return render(request, 'iapp_group/details.html', context)
>>>>>>> d3853e99c5648be50413eebaa536d0761dd5f661
