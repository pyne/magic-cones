from __future__ import print_function
from collections import OrderedDict

from utils import SAPLINGS_PER_CONE, TREES_PER_CONE, inventories

SPELLBOOK = OrderedDict()

def cast(trans, player, spell, target=None):
    """Casts a spell, possibly at a given target"""
    invs = inventories(trans)
    if player not in invs:
        raise ValueError('{0} is not playing magic cones, too bad!'.format(player))
    #if (target is not None) and (target not in invs):
    #    raise ValueError('Target {0} is not playing magic cones!'.format(target))
    inv = invs[player]
    if inv['magic'].get(spell, 0) == 0:
        raise ValueError('{0} does not have any {1} cones!'.format(player, spell))
    if spell not in SPELLBOOK:
        raise ValueError('The eldritch magic of the fabled {0} cone '
                         'has yet-to-be discovered.'.format(spell))
    SPELLBOOK[spell](trans, player, spell, target=target)

def _common_cone(n, trans, player, spell, target=None):
    hist = trans['history']
    if target is None or target == player:
        hist.append({'player': player, 'cones': n, 'kind': spell, 
                     'magic': {spell: -1}})
    else:
        hist.append({'player': player, 'cones': 0, 'kind': spell, 
                     'magic': {spell: -1}, 'target': target})
        hist.append({'player': target, 'cones': n, 'kind': spell, 'target': player})

def cone(trans, player, spell, target=None):
    """adds a single cone to a player (default) or target (optional)."""
    _common_cone(1, trans, player, spell, target=target)

SPELLBOOK['cone'] = cone

def sapling(trans, player, spell, target=None):
    """adds a sapling to a player (default) or target (optional)."""
    _common_cone(SAPLINGS_PER_CONE, trans, player, spell, target=target)

SPELLBOOK['sapling'] = sapling

def tree(trans, player, spell, target=None):
    """adds a tree to a player (default) or target (optional)."""
    _common_cone(TREES_PER_CONE, trans, player, spell, target=target)

SPELLBOOK['tree'] = tree

def counter(trans, player, spell, target=None):
    """cancels the effect of the previously played magic cone."""
    hist = trans['history']
    hist.append({'player': player, 'kind': spell, 'magic': {spell: -1},})
    i = -2
    while (hist[i+1].get('kind', None) == 'counter') and (i > -len(hist)):
        hist[i]['countered'] = not hist[i].get('countered', False)
        i -= 1

SPELLBOOK['counter'] = counter

def clone(trans, player, spell, target=None):
    """clones all of cones from target pull request and gives them to the caster.
    This includes the bounty and the cones from all reviewers.
    """
    if target is None:
        raise ValueError("clone cone requires a pull request number")
    target = int(target)
    n = 0
    hist = trans['history']
    for tran in hist:
        if tran.get('pr', -1) != target:
            continue
        if tran.get('countered', False):
            continue
        if tran.get('kind', '') == 'bounty_poster': 
            continue
        n += tran.get('cones', 0)
    hist.append({'player': player, 'kind': spell, 'cones': n, 'pr': target})

SPELLBOOK['clone'] = clone

def _common_xfer(frac, trans, player, spell, target=None):
    hist = trans['history']
    if target is None or target == player:
        hist.append({'player': player, 'cones': 0, 'kind': spell, 
                     'magic': {spell: -1}})
    else:
        invs = inventories(trans)
        n = int(invs[player]['cones'] * frac)
        hist.append({'player': player, 'cones': -n, 'kind': spell, 
                     'magic': {spell: -1}, 'target': target})
        hist.append({'player': target, 'cones': n, 'kind': spell, 'target': player})

def feed(trans, player, spell, target=None):
    """transfers 1/8 of the casters cones to the target."""
    _common_xfer(0.125, trans, player, spell, target=target)

SPELLBOOK['feed'] = feed

def cede(trans, player, spell, target=None):
    """transfers 1/4 of the casters cones to the target."""
    _common_xfer(0.25, trans, player, spell, target=target)

SPELLBOOK['cede'] = cede

def deed(trans, player, spell, target=None):
    """transfers 1/2 of the casters cones to the target."""
    _common_xfer(0.5, trans, player, spell, target=target)

SPELLBOOK['deed'] = deed

def meed(trans, player, spell, target=None):
    """transfers all of the casters cones to the target."""
    _common_xfer(1.0, trans, player, spell, target=target)

SPELLBOOK['meed'] = meed

