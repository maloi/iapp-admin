from ldapiapp import LdapIapp, entry_from_ldap
from django.conf import settings
import re

class Group():
    
    MULTIVALUE_ATTRS = ['memberUid']
    
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @staticmethod
    def all(attributes = []):
        groups = []
        system_groups = []
        ldap = LdapIapp()
        search_result = ldap.getEntries(settings.LDAP_GROUP_DN, '(cn=*)', attributes)
        for group in search_result:
            # schiebt windowssystem gruppen ins abseits, regex sollte verbessert werden, ggf. anderes ausschlusskriterium
            if re.match(r'^[A-Z]', group['cn'][0]):
                system_groups.append(entry_from_ldap(Group, group, attributes))
            else:
                groups.append(entry_from_ldap(Group, group, attributes))
        return groups

    @staticmethod
    def kind_of(search_filter):
        pass

    @staticmethod
    def get_by_cn(cn, attributes = []):
        ldap = LdapIapp()
        search_result = ldap.getEntries(settings.LDAP_GROUP_DN, 'cn={0}'.format(cn), attributes)
        group = search_result[0]
        return entry_from_ldap(Group, group, attributes)

