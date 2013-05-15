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
    group = Group.get_by_cn(cn, ['cn', 'gidNumber', 'memberUid'])
    members = []
    for memberUid in group.memberUid:
        members.append(User.get_by_uid(memberUid, ['cn', 'uid']))
    context = {
              'group': group,
              'members': members,
              }
    return render(request, 'iapp_group/details.html', context)
