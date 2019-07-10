from typing import Union

from apis import Api
from structures.projects import PypiProject
from structures.versions import PypiRelease


class Pypi(Api):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # set the base url for pypi's api
        self._base_api_url = 'https://pypi.org'

    def request(self, url, **kwargs) -> Union[dict, list]:
        """Manages API rate limitations before calling super().request()."""

        # Note: The pypi json api does not currently have any sort of
        # rate limiting policies in effect. See:
        # https://warehouse.readthedocs.io/api-reference/#rate-limiting
        if self._base_api_url in url:
            # implement any internal rate limiting here...
            pass

        return super().request(url, **kwargs)

    def _make_api_url(self, project: PypiProject) -> str:
        # get the package name and convert to api url
        if 'name' in project.uuids_:
            name = project.uuids_['name']()

        else:
            # extract the name from the url
            name = project.uuids_['url']().strip('/').split('/')[-2]

        return '%s/pypi/%s/json' % (self._base_api_url, name)

    def get_project(self, project: PypiProject, **kwargs) -> None:
        """Gets a project's metadata."""

        # load the url from cache or the web
        url = self._make_api_url(project)
        data = self.request(url, **kwargs)

        # ignore version-related data
        data.pop('releases')

        # break out the contents of the 'info' dict
        data.update(data.pop('info'))

        # update the project
        project.update(**data)

    def get_versions(self, project: PypiProject,
                     historical: str = 'all', **kwargs) -> None:
        """Gets a project's historical releases."""

        # load the url from cache or from the web
        url = self._make_api_url(project)
        data = self.request(url, **kwargs)
        releases = data['releases']

        if historical == 'latest':
            # trim the new versions data to the latest release only
            latest_key: str = data['info']['version']
            releases = {latest_key: releases[latest_key]}

        for v_str, v_data in releases.items():
            # Note: The pypi api returns versions as a dict mapping of
            # version strings to lists of dicts of versions (ie, a single
            # release could have more than one release in a version; eg,
            # a tar.gz and a wheel dist). For now, we'll just take the
            # first dict in the list.
            if v_data:
                v_data = v_data[0]
            else:
                # some releases are missing all info other than their
                # version string
                v_data = {}

            # add the version string to the data dict
            v_data['version'] = v_str

            # add the data to the version
            release = project.find_version(**v_data)
            if historical == 'latest':
                # trim existing releases to the latest release only
                project.versions = [release] if release else []

            if release:
                # update the existing release
                release.update(**v_data)

            else:
                # create a new release
                uuids = {
                    'version': lambda v: v.version
                }
                release = PypiRelease(uuids_=uuids, **v_data)
                project.versions.append(release)
