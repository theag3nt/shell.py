#!/usr/bin/env python

import sys, subprocess

class Shell(object):

    """
    Wrapper object around Popen.

    Usage:

        >>> sh = Shell()
        >>> sh(command, *args, **kwargs)    ->  <command> <kwargs> <args>
        >>> sh.command(*args, **kwargs)     ->  <command> <kwargs> <args>

    Examples:

        >>> sh = Shell()
        >>> sh.ls('*.txt')                  # ls *.txt
        >>> sh.uname("-a")                  # uname -a
        >>> sh.uname(_a=None)               # uname -a
        >>> sh.ping('127.0.0.1', _c=1)      # ping -c 1 127.0.0.1
        >>> sh.cut(_d='"\t"', _f=2)         # cut -d "\t" -f 2
        >>> sh.cut(**{'-d':'"\t"', '-f':2}) # cut -d "\t" -f 2
        >>> sh("ps -x")                     # ps -x

    Modes:

        Shell(Shell.POPEN) (default)

            Returns a Popen object for the command.

        Shell(Shell.OUTPUT)

            Returns the output of the command.

        Shell(Shell.BOOL)

            Returns True if the return code of the command is 0, else False.

    Parsing:

        Arguments:

            Appended to command line without modification after the keyword
            arguments.

        Keyword arguments:

            If the key starts with an underscore, all the underscores in the
            key gets replaced with a hypen.

            If the value coerces to True, it gets appended to the command line
            after the key.

                    _f=None  ->  "-f"
                __foo="bar"  ->  "--foo bar"
            __foo_bar="baz"  ->  "--foo-bar baz"
              foo_bar="baz"  ->  "foo_bar baz"
    """
    
    BOOL    = 0
    OUTPUT  = 1
    POPEN   = 2
    
    def __init__(self, return_type=POPEN):
        self.return_type = return_type
    
    def __call__(self, command, *args, **kwargs):
        command_line = [command]
        for key, value in kwargs.iteritems():
            if key.startswith("_"):
                key = key.replace("_", "-")
            command_line.append(key)
            if value:
                command_line.append(value)
        command_line += args
        if len(command_line) > 1:
            command_line = map(str, command_line)
        else:
            command_line = command_line[0]
        if self.return_type == Shell.BOOL:
            return subprocess.call(command_line, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=(sys.platform=="win32")) == 0
        elif self.return_type == Shell.OUTPUT:
            try:
                return subprocess.check_output(command_line, stderr=subprocess.STDOUT, shell=(sys.platform=="win32"))
            except subprocess.CalledProcessError as e:
                return e.output
        else:
            return subprocess.Popen(command_line, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=(sys.platform=="win32"))
    
    def __getattr__(self, command):
        def wrapper(*args, **kwargs):
            if command.startswith("_"):
                return self(command.lstrip("_").replace("_", "-"), *args, **kwargs)
            return self(command, *args, **kwargs)
        return wrapper
