from django.http import HttpResponse

from lib.ldapiapp import LdapIapp

def index(request):
    ldap = LdapIapp()
    output = ldap.getPeople()
    return HttpResponse(output)
