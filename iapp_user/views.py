from django.http import HttpResponse

from lib.user import User

def index(request):
    output = User.all()
    return HttpResponse(output)

def user(request, uid):
    user = User.get_by_uid(uid, ['cn', 'uid', 'uidNumber'])
    output = user.uid + ' ' + user.cn + ' ' + user.uidNumber
    return HttpResponse(output)
