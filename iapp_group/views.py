from django.http import HttpResponse
from lib.group import Group

def index(request):
    output = Group.all()
    return HttpResponse(output)