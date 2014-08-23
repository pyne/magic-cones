from __future__ import print_function
import io
import os
import re
from getpass import getuser, getpass

from github3 import GitHub, pull_request, repository
import github3.events

from utils import newoverwrite

BOUNTY_RE = re.compile('\*?\*?[Bb][Oo][Uu][Nn][Tt][Yy]\*?\*?\s*[:=-]*?\s*(\d+)')

def gh_make_token(gh, user, credfile='gh.cred'):
    """Creates a github token for the user.

    Parameters
    ----------
    gh : GitHub object
        The object to authenticate with.
    user : str
        The username to make the token for.
    credfile : str, optional
        The github credentials file name.
    
    """
    password = False
    while not password:
        password = getpass("{0}'s github password: ".format(user))
    note = 'magic cones'
    note_url = 'pyne.io'
    scopes = ['user', 'repo']
    auth = gh.authorize(user, password, scopes, note, note_url)
    newoverwrite(str(auth.token) + '\n' + str(auth.id) + '\n', credfile)

def ensure_logged_in(gh, user=None, credfile='gh.cred'):
    """Ensures that the user is logged in, either through a token or by 
    creating a token.

    Parameters
    ----------
    gh : GitHub object
        The object to authenticate with.
    user : str, None, or NotSpecified, optional
        The username to log into github with
    credfile : str, optional
        The github credentials file name.
    """
    if user is None or user is NotSpecified:
        user = getuser()
        print("github username not specified, found {0!r}".format(user))
    if not os.path.isfile(credfile):
        gh_make_token(gh, user, credfile=credfile)
    with io.open(credfile, 'r') as f:
        token = f.readline().strip()  
        id = f.readline().strip()
    gh.login(username=user, token=token)

def update(trans, user=None, credfile='gh.cred'):
    """Takes a list of transactions and updates it with the latest PRs."""
    hist = trans['history']
    previous_prs = set(trans.get('pull_requests', set()))
    gh = GitHub()
    ensure_logged_in(gh, user=user, credfile=credfile)
    r = gh.repository(trans['owner'], trans['repo'])
    #import pdb; pdb.set_trace()
    for pr in r.iter_pulls(state='closed', direction='asc'):
        if pr.number in previous_prs:
            # prevents excessive queries
            continue
        pr.refresh()
        if pr.merged_by is None:
            continue
        num = pr.number
        print("Tallying PR {0}".format(num))
        previous_prs.add(num)
        is_self_merge = (pr.user == pr.merged_by)
        unames = {pr.user.name}
        for comment in pr.iter_comments():
            unames.add(comment.user.name)
        if is_self_merge:
            # no cones awarded for self-merges
            unames.discard(pr.user.name)
        for u in unames:
            tran = {'player': u, 'pr': num, 'cones': 1}
            tran['kind'] = 'requester' if u == pr.user.name else 'reviewer'
            hist.append(tran)
        # apply bounties
        m = BOUNTY_RE.search(pr.body_text)
        if m is not None and not is_self_merge:
            bounty = int(m.group(1))
            hist.append({'player': pr.user.name, 'pr': num, 'cones': -bounty, 
                         'target': pr.merged_by.name, 'kind': 'bounty_poster'})
            hist.append({'player': pr.merged_by.name, 'pr': num, 'cones': bounty, 
                         'target': pr.user.name, 'kind': 'bounty_winner'})
        trans['pull_requests'] = sorted(previous_prs)

