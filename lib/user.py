from ldapiapp import LdapIapp
from django.conf import settings

class User():

    MULTIVALUE_ATTRS = ['objectClass']
    PRIVATE_ATTRS = ['userPassword', 'sambaLMPassword', 'sambaNTPassword']

    def __init__(self, *args, **kwargs):
        setattr(self, 'all_fields', [])
        for key, value in kwargs.items():
            setattr(self, key, value)
            self.all_fields.append(key)

    @staticmethod
    def all(attributes = []):
        users = []
        ldap = LdapIapp()
        search_result = ldap.getEntries(settings.LDAP_USER_DN, '(uid=*)', attributes)
        for user in search_result:
            users.append(user_from_ldap(user, attributes))
        return users

    @staticmethod
    def get_by_uid(uid, attributes = []):
        ldap = LdapIapp()
        search_result = ldap.getEntries(settings.LDAP_USER_DN, 'uid={0}'.format(uid), attributes)
        user = search_result[0]
        return user_from_ldap(user, attributes)

    def showable_attrs(self):
        return [attr for attr in self.all_fields if attr not in self.PRIVATE_ATTRS]

def user_from_ldap(search_result, attributes):
    kwargs = {}
    get_all = False
    if len(attributes) == 0:
        get_all = True
    for key, value in search_result.items():
        if not key in User.MULTIVALUE_ATTRS:
            value = value[0]
        if not get_all and key in attributes:
            kwargs[key] = value
            attributes = [x for x in attributes if x != key]
        else:
            kwargs[key] = value
        for key in attributes:
            kwargs[key] = ''
    return User(**kwargs)

