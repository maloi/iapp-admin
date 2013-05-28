from ldapiapp import LdapIapp, entry_from_ldap
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
            users.append(entry_from_ldap(User, user, attributes))
        return users

    @staticmethod
    def get_by_uid(uid, attributes = []):
        ldap = LdapIapp()
        search_result = ldap.getEntries(settings.LDAP_USER_DN, 'uid={0}'.format(uid), attributes)
        if not search_result:
            return None
        user = search_result[0]
        return entry_from_ldap(User, user, attributes)

    def showable_attrs(self):
        return set(self.all_fields) - set(self.PRIVATE_ATTRS)

