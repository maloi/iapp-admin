from ldapiapp import LdapIapp
from django.conf import settings

class User():

    MULTIVALUE_ATTRS = ['objectclass']

    def __init__(self, *args, **kwargs):
        self._uid        = kwargs.get('uid', "")
        self._cn         = kwargs.get('cn', "")
        self._uid_number = kwargs.get('uid_number', "")
        self._gid_number = kwargs.get('gid_number', "")

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, value):
        self._uid = value

    @property
    def cn(self):
        return self._cn

    @cn.setter
    def cn(self, value):
        self._cn = value

    @property
    def uid_number(self):
        return self._uid_number

    @uid_number.setter
    def uid_number(self, value):
        self._uid_number = value

    @property
    def gid_number(self):
        return self._gid_number

    @gid_number.setter
    def gid_number(self, value):
        self._gid_number = value

    @staticmethod
    def all(attributes = []):
        users = []
        ldap = LdapIapp()
        search_result = ldap.getEntries(settings.LDAP_USER_DN, 'uid=*', attributes)
        for user in search_result:
            users.append(user_from_ldap(user, attributes))
        return users

    @staticmethod
    def get_by_uid(uid, attributes = []):
        ldap = LdapIapp()
        search_result = ldap.getEntries(settings.LDAP_USER_DN, 'uid={0}'.format(uid), attributes)
        user = search_result[0]
        return user_from_ldap(user, attributes)

    def __unicode__(self):
        return "{0}".format(self._uid)

    def __str__(self):
        return "{0}".format(self._uid)


def user_from_ldap(search_result, attributes):
    kwargs = {}
    for attr in attributes:
        result_value = search_result.get(attr, [''])
        if attr in User.MULTIVALUE_ATTRS:
            kwargs[attr] = search_result.get(attr, [''])
        else:
            kwargs[attr] = search_result.get(attr, [''])[0]
    return User(**kwargs)

