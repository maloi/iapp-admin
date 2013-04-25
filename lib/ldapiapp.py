import ldap
from django.conf import settings

class LdapIapp:
    def __init__(self):
        self.ip = settings.AUTH_LDAP_SERVER_URI
        self.binddn = settings.AUTH_LDAP_BIND_DN
        self.bindpw= settings.AUTH_LDAP_BIND_PASSWORD
        self.scope = ldap.SCOPE_SUBTREE
        self.ldapvers = ldap.VERSION3
        
        try:
            self.lcon = ldap.initialize(self.ip)
            self.lcon.simple_bind(self.binddn, self.bindpw)
            self.lcon.protocol_version = self.ldapvers
        except ldap.LDAPError as e:
            return e
        
    def __del__(self):
        self.lcon.unbind()
     
    # allgemeingueltige suche, angabe aller parameter bei aufruf
    def getEntries(self, basedn, filter, attributes):
        try:
            r = self.lcon.search_s(basedn, self.scope, filter, attributes)
            result = []
            for values in r:
                result.append(values[1])
            return result
        except ldap.LDAPError as e:
            return e
            
    # vorgefertigte suchanfragen
    def getPeople(self):
        result = self.getEntries('ou=People,dc=iapp-intern,dc=de', 'uid=*', ['uid', 'cn'])
        return self.sortPeopleUid(result)
    
    def getPeopleInfo(self, uid):
        result = self.getEntries('ou=People,dc=iapp-intern,dc=de', 'uid=' + uid, ['uid', 'cn'])
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