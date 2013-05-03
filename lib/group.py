from ldapiapp import LdapIapp
from django.conf import settings

class Group():
    
    MULTIVALUE_ATTRS = ['memberUid']
    
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @staticmethod
    def all(attributes = []):
        groups = []
        ldap = LdapIapp()
        search_result = ldap.getEntries(settings.LDAP_GROUP_DN, '(cn=*)', attributes)
        for group in search_result:
            groups.append(group_from_ldap(group, attributes))
        return groups

    @staticmethod
    def kind_of(search_filter):
        pass

    @staticmethod
    def get_by_cn(cn, attributes = []):
        ldap = LdapIapp()
        search_result = ldap.getEntries(settings.LDAP_GROUP_DN, 'cn={0}'.format(cn), attributes)
        group = search_result[0]
        return group_from_ldap(group, attributes)


def group_from_ldap(search_result, attributes):
    kwargs = {}
    get_all = False
    if len(attributes) == 0:
        get_all = True
    for key, value in search_result.items():
        if not key in Group.MULTIVALUE_ATTRS:
            value = value[0]
        if not get_all and key in attributes:
            kwargs[key] = value
            attributes = [x for x in attributes if x != key]
        else:
            kwargs[key] = value
        for key in attributes:
            kwargs[key] = ''
    return Group(**kwargs)