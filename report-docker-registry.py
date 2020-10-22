#!/usr/bin/env python

import argparse
import requests
from functools import partial

try:
    # noinspection PyCompatibility
    from urllib.parse import urljoin
except ImportError:
    # noinspection PyUnresolvedReferences,PyCompatibility
    from urlparse import urljoin


def get_paged_objects(self, *args, **kwargs):
    objects = []

    r = self.get(*args, **kwargs)
    while r:
        for obj in r.json():
            objects.append(obj)

        if 'next' in r.links:
            r = self.get(r.links['next']['url'])
        else:
            break

    return objects


# Add the function to Session
requests.Session.get_paged_objects = get_paged_objects


def GitLabSession(prefix=None, token=None):
    if prefix is None:
        prefix = ""
    else:
        prefix = prefix.rstrip('/') + '/'

    def new_request(prefix, f, method, url, *args, **kwargs):
        url = urljoin(prefix, url)
        return f(method, url, *args, **kwargs)

    s = requests.Session()
    s.headers.update({'PRIVATE-TOKEN': token})
    s.request = partial(new_request, prefix, s.request)

    return s


def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def parse_arguments(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(description='Reporting Docker container images in the GitLab registry')

    parser.add_argument('--api', help='API Base URL for your GitLab instance', default='https://gitlab.com/api')
    parser.add_argument('--token', help='Personal API Token to use for authentication', required=True)

    return parser.parse_args(args)


def main():
    args = parse_arguments()

    session = GitLabSession(args.api, token=args.token)

    groups = session.get_paged_objects('v4/groups', params={'top_level_only': True, 'order_by': 'path'})

    overall = 0

    for group in groups:
        header = False

        repos = session.get_paged_objects('v4/groups/%d/registry/repositories' % group['id'])
        total = 0

        for repo in repos:
            if not header:
                print('## %s\n' % group['full_path'])
                header = True

            path = repo['path']

            tags = session.get_paged_objects('v4/projects/%d/registry/repositories/%d/tags' %
                                             (repo['project_id'], repo['id']))

            for tag in tags:

                details = session.get('v4/projects/%d/registry/repositories/%d/tags/%s' %
                                      (repo['project_id'], repo['id'], tag['name'])).json()

                total += details['total_size']

                print("%s:%s\t%s" % (path, tag['name'], sizeof_fmt(details['total_size'])))

        if total > 0:
            print("\nTotal for group: %s\n" % sizeof_fmt(total))
            overall += total

    if overall > 0:
        print("## Total\n\n%s\n" % sizeof_fmt(overall))

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
