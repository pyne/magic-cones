#!/usr/bin/env python
from __future__ import print_function
import io
import os
import sys
import json
import argparse

import github

def main():
    parser = argparse.ArgumentParser('magic-cones')
    parser.add_argument('-r', '--repo', help='owner/repo string', 
                        dest='repo')
    parser.add_argument('-t', '--transactions', help='/path/to/transactions file', 
                        default='trans.json', dest='transactions_fname')
    parser.add_argument('--update', action='store_true', default=False, dest='update',
                        help='updates transactions from github')
    parser.add_argument('--gh-user', default=None, dest='gh_user',
                        help='github username')
    parser.add_argument('--gh-cred', default='gh.cred', dest='gh_cred',
                        help='github credentials file')
    ns = parser.parse_args()

    if os.path.isfile(ns.transactions_fname):
        with io.open(ns.transactions_fname, 'rt') as f:
            trans = json.load(f)
    else:
        if ns.repo is None:
            raise ValueError ('--repo must be given')
        owner, repo = ns.repo.split('/', 1)
        trans = {'owner': owner, 'repo':  repo, 'history': []}

    if ns.update:
        github.update(trans, user=ns.gh_user, credfile=ns.gh_cred)

    with io.open(ns.transactions_fname, 'wb') as f:
        json.dump(trans, f, indent=1, separators=(',', ': '))


if __name__ == '__main__':
    main()