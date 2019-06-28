import json

from file_types import FileType
from structures import Dataset


file_formats = {
    'GitRepo': {},
    'GitRepoCommit': {},
    'HttpUrl': {},
    'PackageVersion': {}
}


class JsonFileType(FileType):
    @staticmethod
    def load(dataset: Dataset, path: str, file_format: str = None) -> None:
        """Default json parser."""

        # load the file
        raw = json.load(open(path))

        # if not user defined, determine the json input type
        file_format = file_format or \
                      raw.get('inputs', [{}])[0].get('input_type', None)
        if not file_format:
            ex = 'Json parsing schema could not be determined.'
            raise Exception(ex)

        # we have a parsing schema for the input type
        if file_format not in file_formats:
            raise Exception('Invalid json parsing schema.')

        # load the appropriate input schema
        schema = file_formats[file_format]

        stop = 'here'

    @staticmethod
    def save(dataset: Dataset, name: str = ''):
        """Writes a dataset to json. Unique to json filetype."""
        pass
