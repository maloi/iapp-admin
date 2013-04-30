from django.http import HttpResponse

from lib.user import User

def index(request):
    users = User.all()
    output = ''
    for user in users:
        output += user.uid + ' '
        if hasattr(user, 'cn'):
            output += user.cn + '<br>'
    return HttpResponse(output)

def user(request, uid):
    user = User.get_by_uid(uid, ['cn', 'uid', 'uidNumber'])
    user2 = User.get_by_uid(uid)
    output = user.uid + ' ' + user.cn + ' ' + user.uidNumber
    output2 = user2.uid + ' ' + user2.cn + ' ' + user2.gidNumber
    return HttpResponse(output + '<br>' + output2)
