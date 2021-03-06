import ldap
import ldap.modlist
from django.conf import settings

class LdapIapp(object):
    def __init__(self):
        self.ip = settings.AUTH_LDAP_SERVER_URI
        self.binddn = settings.AUTH_LDAP_BIND_DN
        self.bindpw= settings.AUTH_LDAP_BIND_PASSWORD
        self.scope = ldap.SCOPE_SUBTREE
        self.ldapvers = ldap.VERSION3
        
        try:
            self.lcon = ldap.initialize(self.ip)
            self.lcon.simple_bind_s(self.binddn, self.bindpw)
            self.lcon.protocol_version = self.ldapvers
        except ldap.LDAPError as e:
            return e
        
    def __del__(self):
        self.lcon.unbind()

    # allgemeingueltige suche, angabe aller parameter bei aufruf
    def getEntries(self, basedn, filters, attributes):
        r = self.lcon.search_s(basedn, self.scope, filters, attributes)
        if not r:
            return None
        result = []
        for values in r:
            result.append(values[1])
        return result
    
    # schreibt neuen Wert in LDAP
    def setEntries(self, dn, old, new):
        ldif = ldap.modlist.modifyModlist(old, new)
        self.lcon.modify_s(dn, ldif)
        return True
        

    # vorgefertigte suchanfragen
    def getPeople(self):
        result = self.getEntries(settings.LDAP_USER_DN, 'uid=*', ['uid', 'cn'])
        return self.sortPeopleUid(result)
    
    def getPeopleInfo(self, uid):
        result = self.getEntries(settings.LDAP_USER_DN, 'uid=' + uid, ['uid', 'cn'])
        return result[0]
    
    def getMaillist(self):
        entries = self.getEntries(settings.LDAP_MAILLIST_DN, 'cn=*', ['cn', ])
        list_entries = []
        for value in entries:
            list_entries.append(value['cn'][0])
        result = {'name' : list_entries, 'count' : len(list_entries)}
        return result

    def getMaillistInfo(self, list):
        maillist = self.getEntries(settings.LDAP_MAILLIST_DN, 'cn=' + list, ['cn', 'mail', 'owner', 'member'])
        peoples = self.getPeople()
        result = {'owner' : [], 'members' : []}
        for k, v in maillist[0].items():
            if k == 'member':
                for value in v:
                    user = value.split(',')
                    uid = user[0][4:]
                    if uid in peoples:
                        result['members'].append(peoples[uid]['cn'])
                    else:
                        pass
            elif k == 'owner':
                for value in v:
                    user = value.split(',')
                    uid = user[0][4:]
                    if uid in peoples:
                        result['owner'].append(peoples[uid]['cn'])
                    else:
                        pass
            elif k == 'mail':
                result['mail'] = v
            elif k == 'cn':
                result['cn'] = v
            else:
                #errorhandlig
                pass
        return result
    
    # Sortierung der Informationen aller Art
    def sortPeopleUid(self, people):
        result = {}
        for values in people:
            if 'cn' in values:
                result[values['uid'][0]] = {'uid' : values['uid'][0], 'cn' : values['cn'][0]}
            else:
                continue
        return result


def entry_from_ldap(entry, search_result, attributes):
    kwargs = {}
    get_all = False
    if len(attributes) == 0:
        get_all = True
    for key, value in search_result.items():
        if not key in entry.MULTIVALUE_ATTRS:
            value = value[0]
        if not get_all and key in attributes:
            kwargs[key] = value
            attributes = [x for x in attributes if x != key]
        else:
            kwargs[key] = value
        for key in attributes:
            kwargs[key] = ''
    return entry(**kwargs)


