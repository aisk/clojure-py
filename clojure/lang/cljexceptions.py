class AbstractMethodCall(Exception):
    def __init__(self, cls=None):
        if cls is not None:
            Exception.__init__(self, "in " + cls.__class__.__name__)
        else:
            Exception.__init__(self)


class ArityException(TypeError):
    def __init__(self, s=None):
        TypeError.__init__(self, s)


class CljException(Exception):
    def __init__(self, s=None):
        Exception.__init__(self, s)


class IllegalStateException(CljException):
    pass


class InvalidArgumentException(CljException):
    pass


class IllegalAccessError(CljException):
    pass


class IndexOutOfBoundsException(CljException):
    pass


class UnsupportedOperationException(Exception):
    pass


class IllegalArgumentException(Exception):
    pass


class ReaderException(Exception):
    def __init__(self, s=None, rdr=None):
        Exception.__init__(self,
                           s + ("" if rdr is None
                                else " at line " + str(rdr.lineCol()[0])))


class CompilerException(Exception):
    def __init__(self, reason, form):
        from lispreader import LINE_KEY
        msg = "Compiler exception {0}".format(reason)
        at = getattr(form, "meta", lambda: {LINE_KEY: None})()[LINE_KEY]
        if at:
            msg += " at {0}".format(at)
        Exception.__init__(self, msg)
