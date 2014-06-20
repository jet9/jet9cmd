
class Jet9CmdProxy(object):
    def __init__(self):
        """Constructor: returns pattern for commands"""

        pass

    @staticmethod
    def cmd_path():
        """ Returns cmd path pattern """

        return {
            "proxy:Manage proxy settings": {
                "redirect_error:Redirect all Web HTTP requests for user to error page": [ "user" ],
                "peer:": {
                    "add:Add peer for user/domain": [ "user", "domain" ],
                    "remove:Remove peer for user/domain": [ "user", "domain" ],
                    "list:List peers list for user": [ "user" ],
                },
            },
        }

    def redirect_error(self, subcmd, user):
        """ cmd routine """

        print "subcmd: {0} redirect_error: {1}".format(subcmd, user)

    def peer(self, subcmd, **kwarg):
        """ peer cmd routine """

        print "subcmd: {0} peer: {1}".format(subcmd, kwarg)

# mapping for autoregister module in j9sh
mapping = { "proxy": Jet9CmdProxy }

