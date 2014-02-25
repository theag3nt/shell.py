shell.py
========

Simple wrapper around Python's Popen.

Usage
-----

```python
>>> sh = Shell()
>>> sh(command, *args, **kwargs)    # <command> <kwargs> <args>
>>> sh.command(*args, **kwargs)     # <command> <kwargs> <args>
```

Examples
--------

```python
>>> sh = Shell()
>>> sh.ls('*.txt')                  # ls *.txt
>>> sh.uname("-a")                  # uname -a
>>> sh.uname(_a=None)               # uname -a
>>> sh.ping('127.0.0.1', _c=1)      # ping -c 1 127.0.0.1
>>> sh.cut(_d='"\t"', _f=2)         # cut -d "\t" -f 2
>>> sh.cut(**{'-d':'"\t"', '-f':2}) # cut -d "\t" -f 2
>>> sh("ps -x")                     # ps -x
```

Modes
-----

`Shell(Shell.POPEN)` _(default)_

Returns a Popen object for the command.

`Shell(Shell.OUTPUT)`

Returns the output of the command.

`Shell(Shell.BOOL)`

Returns True if the return code of the command is 0, else False.

Parsing
-------

- Arguments
    
    Appended to command line without modification after the keyword
    arguments.

- Keyword arguments
    
    If the key starts with an underscore, all the underscores in the
    key gets replaced with a hypen.

    If the value coerces to True, it gets appended to the command line
    after the key.

```
        _f=None  ->  "-f"
    __foo="bar"  ->  "--foo bar"
__foo_bar="baz"  ->  "--foo-bar baz"
  foo_bar="baz"  ->  "foo_bar baz"
```