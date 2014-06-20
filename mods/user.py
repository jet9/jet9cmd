
class Jet9CmdUser(object):
    def __init__(self):
        """Constructor: returns pattern for commands"""

        pass

    @staticmethod
    def cmd_path():
        """ Returns cmd path pattern """

        return {
            "user:User management": {
                "info:Show user info": ["user"],
                "list:Show list of users": [],
                "add:Add user to system": ["user", "password", "domain", "tariff"],
                "disable:Disable user in system": ["user"],
                "enable:Enable user in system": ["user"],
                "remove:Remove user from system": ["user"],
                "set_password:": {
                    "main:Set main system passwd for user": [ "user", "password" ],
                    "lcx_root:Set lxc root password for user": [ "user", "password" ],
                },
                "set_tariff:Set user's tariff": [ "user", "tariff" ],
            },
        }

    def info(self, subcmd, user):
        """ info cmd routine """

        print "subcmd: {0} info: {1}".format(subcmd, user)

    def enable(self, subcmd, user):
        """ info cmd routine """

        print "subcmd: {0} info: {1}".format(subcmd, user)

    def disable(self, subcmd, user):
        """ info cmd routine """

        print "subcmd: {0} info: {1}".format(subcmd, user)

# mapping for autoregister module in j9sh
mapping = { "user": Jet9CmdUser }

