from ldapiapp import LdapIapp
from django.conf import settings

class User():

    def __init__(self,
                 uid,
                 cn,
                 uid_number='',
                 gid_number='',
                ):
        self._uid        = uid
        self._cn         = cn
        self._uid_number = uid_number
        self._gid_number = gid_number

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
    def all():
        users = []
        ldap = LdapIapp()
        search_result = ldap.getEntries(settings.LDAP_USER_DN, 'uid=*', ['uid', 'cn'])
        for user in search_result:
            cn = user.get('cn', [''])
            uid = user.get('uid', [''])
            users.append(User(uid[0], cn[0]))
        return users

    def __unicode__(self):
        return "{0}".format(self._uid)
    def __str__(self):
        return "{0}".format(self._uid)
