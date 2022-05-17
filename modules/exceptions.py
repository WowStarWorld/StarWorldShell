import sys

class CommandNotFoundError(Exception): __module__="builtins"
class ExitError(Exception): __module__="builtins"
class PluginNotFoundError(Exception): __module__="builtins"

def exception_format():
    return sys.exc_info()[0].__name__ + ": " + str(sys.exc_info()[1]) if str(sys.exc_info()[1]) != "" else \
        sys.exc_info()[0].__name__