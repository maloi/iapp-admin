from ldapiapp import LdapIapp
from django.conf import settings

class User():

    ATTRS = {
            'shadowMin': {
                'help': "",
                'default': "",
                         },
            'uid':       {
                'help': "Login",
                'default': "",
                         },
            'jpegPhoto': {
                'help': "Picture of User",
                'default': "",
                         },
            'uidNumber': {
                'help': "User ID",
                'default': "",
                         },
            'sambaAcctFlags': {
                'help': "",
                'default': "",
                         },
            'sambaPasswordHistory': {
                'help': "",
                'default': "",
                         },
            'deIappNoContract': {
                'help': "",
                'default': "",
                         },
            'deIappNoAutoEmail': {
                'help': "",
                'default': "",
                         },
            'shadowLastChange': {
                'help': "",
                'default': "",
                         },
            'deIappOrder': {
                'help': "Order in IAPP hierarchy",
                'default': "",
                         },
            'cn': {
                'help': "Common name",
                'default': "",
                         },
            'employeeType': {
                'help': "",
                'default': "",
                         },
            'sortName': {
                'help': "Name for sorting the user",
                'default': "",
                         },
            'deIappBlackboard': {
                'help': "Is the user on the blackboard?",
                'default': "",
                         },
            'userPassword': {
                'help': "Password",
                'default': "",
                         },
            'deIappAlias': {
                'help': "Alias for Login for e.g. verbose email address",
                'default': "",
                         },
            'sambaLMPassword': {
                'help': "",
                'default': "",
                         },
            'mail': {
                'help': "Email address in addition to login@iapp.de",
                'default': "",
                             },
            'loginShell': {
                'help': "Shell (e.g. /bin/bash",
                'default': "",
                             },
            'deIappInactive': {
                 'help': "",
                 'default': "",
                             },
            'gidNumber': {
                'help': "",
                'default': "",
                             },
            'deIappNotPublic': {
                'help': "",
                'default': "",
                             },
            'sambaPwdLastSet': {
                'help': "",
                'default': "",
                             },
            'shadowMax': {
                'help': "",
                'default': "",
                             },
            'sambaNTPassword': {
                'help': "",
                'default': "",
                             },
            'telephoneNumber': {
                'help': "",
                'default': "",
                             },
            'deIappBirthday': {
                'help': "",
                'default': "",
                             },
            'displayName': {
                'help': "",
                'default': "",
                             },
            'shadowWarning': {
                'help': "",
                'default': "",
                             },
            'shadowInactive': {
                'help': "",
                'default': "",
                             },
            'sambaHomeDrive': {
                'help': "",
                'default': "",
                             },
            'roomNumber': {
                'help': "",
                'default': "",
                             },
            'sambaSID': {
                'help': "",
                'default': "",
                             },
            'gecos': {
                'help': "",
                'default': "",
                             },
            'sn': {
                'help': "",
                'default': "",
                             },
            'homeDirectory': {
                'help': "",
                'default': "",
                             },
            'givenName': {
                'help': "",
                'default': "",
                             },
            'deIappWebspace': {
                'help': "",
                'default': "",
                             },
            }
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
        return set(self.all_fields) - set(self.PRIVATE_ATTRS)

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

