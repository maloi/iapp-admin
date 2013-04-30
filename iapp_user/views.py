from django.http import HttpResponse

from lib.user import User

def index(request):
    output = User.all()
    return HttpResponse(output)
