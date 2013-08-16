from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from operator import  attrgetter

from lib.group import Group
from lib.user import User
from lib.formulare import GroupForm
import types

@login_required
def index(request):
    all_group = Group.all(['cn', 'gidNumber'])
    sorted_all_group = sorted(all_group, key=attrgetter('cn'))
    context = {'all_group' : sorted_all_group}
    return render(request, 'iapp_group/index.html', context)

@login_required
def group(request, cn, sort_by='sn'):
    group = Group.get_by_cn(cn, ['cn', 'description', 'gidNumber', 'memberUid', 'owner'])
    members = []
    owner = group.owner.split(',')[0][4:]
    description = group.description
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
              'description' : description,
              'group': group,
              'members': sorted_members,
              'owner' : owner,
              }
    return render(request, 'iapp_group/details.html', context)

@login_required
def group_edit(request, cn):
    attrs = ['cn', 'description', 'gidNumber', 'memberUid','owner']
    group = Group.get_by_cn(cn, attrs)
    kwargs = {}
    memberuid = []
    # fuellt formular mit vorhanden daten aus LDAP
    #form = GroupForm()
    for key in attrs:
        kwargs[key] = getattr(group,key)
        if key == 'memberUid':
            for member in kwargs[key]: 
                # haengt mitglieder der gruppe an liste an
                #memberuid.append((member, member))
                memberuid.append(member)
        else:
            pass
    form = GroupForm(initial=kwargs)
    #form.fields['memberUid'].initial = ['leumer', 'mmuench', 'schmidt']
    form_msg = ''
    old = {}
    new = {}
    wert = ['Hallo', 'ich', 'bin', 'Paul']
    typ = type(wert)
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            for key, value in request.POST.items():
                if str(key) in attrs:
                    if str(key) == 'memberUid':
                        #if type(form[str(key)].value) == type(list()):
                        new[str(key)] = [string.encode('utf-8') for string in form.cleaned_data.get(str(key))]
                    else:
                        new[str(key)] = form.cleaned_data.get(str(key)).encode('utf-8')
                    old[str(key)] = getattr(group, str(key))
                    if old[str(key)] != new[str(key)]:
                        Group.write_ldif(cn, old, new)
                        form_msg = 'Formular gueltig.'
                    else:
                        form_msg = 'Es wurde nichts geaendert!'
                else:
                    pass #errorhandling
        else:
            form_msg = 'Formular NICHT gueltig!'
            #form = GroupForm()        
    context = { 'form' : form,
                'form_msg' : form_msg,
                'cn' : cn,
                'new' : new,
                'old' : old,
                'memberuid' : memberuid,
                'typ' : typ,
            }
    return render(request, 'iapp_group/edit.html', context )