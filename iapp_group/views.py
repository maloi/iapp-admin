from django.http import HttpResponse
from django.shortcuts import render

from lib.group import Group
from lib.user import User

#def index(request):
#    groups = Group.all(['cn', ])
#    output = ''
#    for group in groups:
#        output += group.cn + ' '
#        output += group.gidNumber + '<br />'
#    return HttpResponse(output)

def index(request):
    all_group = Group.all(['cn', ])
    context = {'all_group' : all_group}
    return render(request, 'iapp_group/index.html', context)

#def group(request, cn):
#    group = Group.get_by_cn(cn, ['cn', 'gidNumber', 'memberUid'])
#    users = User.all(['uid', 'cn'])
#    uids = ''
#    for uid in group.memberUid:
#        for user in users:
#            if uid in user.uid:
#                uids += '<br />' + user.cn +  ' ' + uid
#    output = group.cn + ' ' + group.gidNumber + ' ' + uids
#    return HttpResponse(output)

def group(request, cn):
    info_group = Group.get_by_cn(cn, ['cn', 'gidNumber', 'memberUid'])
    info_user = User.all(['uid', 'cn'])
    context = {'info_group' : info_group,
                    'info_user' : info_user,}
    return render(request, 'iapp_group/index.html', context)