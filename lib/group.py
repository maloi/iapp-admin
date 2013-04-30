from ldapiapp import LdapIapp
from django.conf import settings

class Group():
    
    def __init__(self,
                    cn,
                    gid_number,
                    ):
        self._cn = cn
        self._gidnumber = gid_number
        
    @property
    def cn(self):
        return self._cn

    @cn.setter
    def cn(self, value):
        self._cn = value

    @property
    def gid_number(self):
        return self._gid_number

    @gid_number.setter
    def gid_number(self, value):
        self._gid_number = value

    @staticmethod
    def all(attr = [] ):
        groups = []
        ldap = LdapIapp()
        search_result = ldap.getEntries(settings.LDAP_GROUP_DN, 'cn=*', attr)
        for group in search_result:
            cn = group.get('cn', [''])
            gid_number = group.get('gidnumber', [''])
            groups.append(Group(cn[0], gid_number[0]))
        return groups

    @staticmethod
    def info(group, attr = [] ):
        ldap = LdapIapp()
        result = ldap.getEntries(settings.LDAP_GROUP_DN, 'cn={0}'.format(group), attr )
        return result

    def __unicode__(self):
        return "{0}".format(self._cn)
    def __str__(self):
        return "{0}".format(self._cn)