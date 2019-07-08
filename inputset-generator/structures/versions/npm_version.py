from structures.versions import Version


class NpmVersion(Version):
    def check_guarantees(self) -> None:
        """Guarantees a version string."""
        if 'version' not in self.meta_:
            raise Exception('Version string must be provided.')
