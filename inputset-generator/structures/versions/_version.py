from types import MethodType


class Version:
    def __init__(self, attrs: dict = None, **kwargs):
        # set the attr functions as method types (to autopass self)
        self.attrs = {}
        for attr, func in attrs.items():
            self.attrs[attr] = MethodType(func, self)

        # load all attributes into the version
        self.update(**kwargs)

    def update(self, **kwargs) -> None:
        """Populates the version with data from a dictionary."""
        for k, val in kwargs.items():
            setattr(self, k, val)

        # make sure all guarantees are met
        self.check_guarantees()

    def check_guarantees(self):
        """Guarantees a version string or commit hash."""
        if 'version' not in self.attrs and 'commit' not in self.attrs:
            raise Exception('Version string or commit hash '
                            'must be provided.')

    def __repr__(self):
        return 'Version(%s)' % ', '.join([
            '%s=%s' % (a, repr(getattr(self, a)))
            for a in dir(self)
            if getattr(self, a)
               and not a.startswith('__')
               and not callable(getattr(self, a))
        ])
