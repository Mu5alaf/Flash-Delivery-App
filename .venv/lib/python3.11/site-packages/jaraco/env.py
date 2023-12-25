import os


class Check:
    """
    Check if an environment variable meets a certain expectation.

    >>> setenv = getfixture('monkeypatch').setenv
    >>> check = Check('SOME_VAR', expect='setting1')
    >>> bool(check)
    False
    >>> setenv('SOME_VAR', 'setting1')
    >>> bool(check)
    True
    >>> setenv('SOME_VAR', 'setting2')
    >>> bool(check)
    False

    >>> check = Check('OTHER_VAR', expect='setting1', default='setting1')
    >>> bool(check)
    True
    >>> setenv('OTHER_VAR', 'setting2')
    >>> bool(check)
    False
    """

    def __init__(self, key, expect, *, default=None, _lookup=os.environ):
        self.key = key
        self.expect = expect
        self.default = default
        self.lookup = _lookup

    def __bool__(self):
        return self.lookup.get(self.key, self.default) == self.expect
