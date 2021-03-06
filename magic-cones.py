#!/usr/bin/env python
from __future__ import print_function
import io
import os
import sys
import json
import argparse

import gaia
import utils
import raven
import github
import report
import lawyer
import grimoire

def main():
    parser = argparse.ArgumentParser('magic-cones')
    parser.add_argument('--repo', help='owner/repo string', 
                        dest='repo')
    parser.add_argument('-t', '--transactions', help='/path/to/transactions file', 
                        default='trans.json', dest='transactions_fname')
    parser.add_argument('--update', action='store_true', default=False, dest='update',
                        help='updates transactions from github')
    parser.add_argument('--drop', action='store_true', default=False, dest='drop',
                        help='Gaia drops magic cones')
    parser.add_argument('--decay', action='store_true', default=False, dest='decay',
                        help='Gaia decays existing cones')
    parser.add_argument('--give', nargs=2, default=(), dest='give',
                        help='gives a player a cones manually')
    parser.add_argument('--kind', default='welfare', dest='kind',
                        help='determines the kind of transaction when manually giving'
                             'a player cones.')
    parser.add_argument('-r', action='store_true', default=False, dest='report',
                        help='prints report')
    parser.add_argument('--html', action='store_true', default=False, dest='html',
                        help='uses html')
    parser.add_argument('--cast', nargs=2, default=(), dest='cast',
                        help='casts a spell, of the form player and magic cone')
    parser.add_argument('--target', default=None, dest='target',
                        help='target of a spell')
    parser.add_argument('--gh-user', default=None, dest='gh_user',
                        help='github username')
    parser.add_argument('--gh-cred', default='gh.cred', dest='gh_cred',
                        help='github credentials file')
    parser.add_argument('--email', action='store_true', default=False, dest='email',
                        help='sends an email summary')
    parser.add_argument('--rules', action='store_true', default=False, dest='rules',
                        help='displays the rules')
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
    if len(ns.give) > 0:
        utils.give_cones(trans, ns.give[0], int(ns.give[1]), kind=ns.kind)
    if ns.drop:
        gaia.drop(trans)
    if ns.decay:
        gaia.decay(trans)
    if len(ns.cast) > 0:
        grimoire.cast(trans, ns.cast[0], ns.cast[1], target=ns.target)
    if ns.report:
        print(report.report(trans, html=ns.html))
    if ns.email:
        raven.send(trans)
    if ns.rules:
        print(lawyer.rules(html=ns.html))

    with io.open(ns.transactions_fname, 'wb') as f:
        json.dump(trans, f, indent=1, separators=(',', ': '))


if __name__ == '__main__':
    main()