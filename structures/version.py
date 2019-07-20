class Version:
    def __init__(self, **kwargs):
        # load all attributes into the version
        self.populate(kwargs)

    def populate(self, data: dict) -> None:
        """Populates the version with data from a dictionary."""
        for k, val in data.items():
            setattr(self, k, val)

    def __repr__(self):
        return 'Version(%s)' % ', '.join([
            '%s=%s' % (a, repr(getattr(self, a)))
            for a in dir(self)
            if getattr(self, a)
               and not a.startswith('__')
               and not callable(getattr(self, a))
        ])
