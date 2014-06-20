#!/usr/bin/env python

import os
import sys

def d(s):
    """simple debug func"""

    #print s
    pass

class Jet9CmdError(Exception):
    pass

class Jet9Cmd(object):
    """ Simple cli wrapper """

    def __init__(self, progname, version, mod_dir="mods"):
        self.mod_dir = mod_dir
        self.version = version
        self.progname = progname
        self.pattern_helps = {}
        self.pattern = {}
        self.mappings = {}
        self.mods = []
        
        self._import_mods()
        self._generate_mapping()
        self._generate_pattern()
        self.pattern = self._strip_pattern(self.pattern_helps)

    def _parse_cmd(self, _cmd):
        """Parse users command string"""

        cmd = list(_cmd)
        tail = dict(self.pattern)
        out = {
            "module": None,
            "command": None,
            "subcommand": None,
            "params": {},
        }

        # get module
        if len(cmd) == 0:
            # Error: empty cmd list
            raise Jet9CmdError("empty cmd list".format(word))

        word = cmd.pop(0)
        d("word={0}".format(word))

        if word not in tail.keys():
            # Error: unknown module name
            raise Jet9CmdError("unknown module name `{0}'".format(word))

        out["module"] = word
        d("module: {0}".format(word))

        tail = tail[word]
        d("tail: {0}".format(tail))

        # get command
        if len(cmd) == 0:
            # Error: empty cmd list
            raise Jet9CmdError("empty cmd list")

        word = cmd.pop(0)
        d("word={0}".format(word))

        if word not in tail.keys():
            # Error: unknown command name
            raise Jet9CmdError("unknown command name `{0}'".format(word))

        out["command"] = word
        d("command: {0}".format(word))

        tail = tail[word]
        d("tail: {0}".format(tail))


        if isinstance(tail, dict):
            # get subcommand
            if len(cmd) == 0:
                return out

            word = cmd.pop(0)
            d("word={0}".format(word))
            d("cmd has subcommand: parsing...")

            if word in tail.keys():
                out["subcommand"] = word
                d("subcommand: {0}".format(word))
                tail = tail[word]
                d("tail: {0}".format(tail))
            else:
                # Error: unknown subcommand
                raise Jet9CmdError("unknown subcommand `{0}'".format(word))

        tail = list(tail)
        # get params
        while 1:
            if len(cmd) == 0:
                if len(tail) > 0:
                    raise Jet9CmdError("not enough params")

                return out

            word = cmd.pop(0)
            d("word={0}".format(word))

            if len(tail) == 0:
                # Error: too much params
                raise Jet9CmdError("too much params")

            d("tail: {0}".format(tail))
            param_name = tail.pop(0)
            d("param_name: {0}".format(param_name))
            out["params"].update({param_name: word})

        return out

    def _import_mods(self):
        """ Import action modules from directory actions """

        for i in os.listdir("./%s/" % (self.mod_dir, )):
            if i.endswith(".py") and not i.startswith("__"):
                modname = i[:-3]
                self.mods.append(__import__(self.mod_dir + "." + modname, fromlist=['mapping']))

    def _generate_mapping(self):
        """ Generate modules class mappings """

        for mod in self.mods:
            self.mappings.update(mod.mapping)

    def _generate_pattern(self):
        """ Generate cmd search pattern from mappings """

        for cls in self.mappings.keys():
            self.pattern_helps.update(self.mappings[cls].cmd_path())

    def process_cmd(self, cmd):
        """ Process cmd """

        try:
            _cmd = self._parse_cmd(cmd)

        except Jet9CmdError as e:
            raise Jet9CmdError("Cmd parsing error: {0}".format(e))

        if _cmd["module"] not in self.mappings.keys():
            raise Jet9CmdError("{0} module not found".format(_cmd["module"]))

        cls_instance = self.mappings[_cmd["module"]]()

        try:
            exit_code = getattr(cls_instance, _cmd["command"])(_cmd["subcommand"], **_cmd["params"])

        except AttributeError:
            raise Jet9CmdError("Cmd process error: command `{0}' not implemented".format(_cmd["command"]))

        if not isinstance(exit_code, int):
            exit_code = 0

        return exit_code

    def _strip_pattern(self, pattern):
        """ Remove help string from pattern keys """

        p = dict(pattern)

        for key in p.keys():
            new_key = key.split(":")[0]
            if isinstance(p[key], dict):
                if new_key in p.keys():
                    p[new_key].update(self._strip_pattern(p[key]))
                else:
                    p[new_key] = self._strip_pattern(p[key])

            elif isinstance(p[key], list):
                p[new_key] = list(p[key])

            del p[key]

        return p

    def _print_cmd_help(self, module, leaf, indent):
        """ Recusively print help for module """

        print " " * indent * 4 + module

        for key in leaf.keys():
            (cmd, helpstr) = key.split(":")
            if isinstance(leaf[key], dict):
                self._print_cmd_help(cmd, leaf[key], indent+1)
            else:
                j = [cmd]
                joined_cmd = cmd + " " + " ".join([param.upper() for param in leaf[key]])
                print " " * (indent+1)*4 + "{0:40s} {1:80s}".format(joined_cmd, helpstr)

    def print_help(self, module=None):
        """ Show help for module(s)"""

        print "Usage: {0} module command [subcommand] [param1, ...]".format(self.progname)
        print "Version: {0}".format(self.version)
        print ""

        if module is None:
            print "modules:"
            for key in self.pattern_helps.keys():
                (mod, helpstr) = key.split(":")
                print "    {0:10s} {1:80s}".format(mod, helpstr)

            print ""
            print "type '{0} help <module>' to show help for specific module".format(self.progname)

        else:
            print "module:"
            for key in self.pattern_helps.keys():
                (mod, helpstr) = key.split(":")
                if mod != module:
                    continue

                self._print_cmd_help(mod, self.pattern_helps[key], 0)

if __name__ == "__main__":

    cmd = Jet9Cmd(progname=sys.argv[0], version="0.1", mod_dir="mods")

    if len(sys.argv) == 1 or sys.argv[1] == "--help" or sys.argv[1] == "-h":
        cmd.print_help()
        sys.exit(0)

    elif sys.argv[1] == "help" and len(sys.argv) > 2:
        cmd.print_help(module=sys.argv[2])
        sys.exit(0)

    try:
       sys.exit(cmd.process_cmd(sys.argv[1:]))

    except Jet9CmdError as e:
        print str(e)
        sys.exit(1)

