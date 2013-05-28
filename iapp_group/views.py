from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from operator import  attrgetter

from lib.group import Group
from lib.user import User

@login_required
def index(request):
    all_group = Group.all(['cn', 'gidNumber'])
    sorted_all_group = sorted(all_group, key=attrgetter('cn'))
    context = {'all_group' : sorted_all_group}
    return render(request, 'iapp_group/index.html', context)

@login_required
def group(request, cn, sort_by='sn'):
    group = Group.get_by_cn(cn, ['cn', 'gidNumber', 'memberUid'])
    members = []
    for memberUid in group.memberUid:
        user = User.get_by_uid(memberUid, ['uid', 'givenName', 'sn'])
        if not user:
            kwargs = {}
            kwargs['uid'] = memberUid
            kwargs['givenName'] = ''
            kwargs['sn'] = ''
            kwargs['former_member'] = True
            user = User(**kwargs)
        members.append(user)
    sorted_members = sorted(members, key=attrgetter(sort_by))
    context = {
              'group': group,
              'members': sorted_members,
              }
    return render(request, 'iapp_group/details.html', context)

@login_required
def group_edit(request, cn):
    group = Group.get_by_cn(cn, ['cn', 'gidNumber', 'memberUid'])
    user = User.all(['uid', 'givenName', 'sn'])
    context = {'group_edit' : group}
    return render(request, 'iapp_group/edit.html', context)
