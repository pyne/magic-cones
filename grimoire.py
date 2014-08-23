from __future__ import print_function

from utils import SAPLINGS_PER_CONE, TREES_PER_CONE, inventories

SPELLBOOK = {}

def cast(trans, player, spell, target=None):
    """Casts a spell, possibly at a given target"""
    invs = inventories(trans)
    if player not in invs:
        raise ValueError('{0} is not playing magic cones, too bad!'.format(player))
    if target is not None and target not in invs and:
        raise ValueError('Target {0} is not playing magic cones!'.format(target))
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
    """cone - adds a single cone to a player (default) or target (optional)."""
    _common_cone(1, trans, player, spell, target=target)

SPELLBOOK['cone'] = cone

def sapling(trans, player, spell, target=None):
    """sapling - adds a sapling to a player (default) or target (optional)."""
    _common_cone(SAPLINGS_PER_CONE, trans, player, spell, target=target)

SPELLBOOK['sapling'] = sapling

def tree(trans, player, spell, target=None):
    """tree - adds a tree to a player (default) or target (optional)."""
    _common_cone(TREES_PER_CONE, trans, player, spell, target=target)

SPELLBOOK['tree'] = tree

def counter(trans, player, spell, target=None):
    """counter - cancels the effect of the previously played magic cone."""
    hist = trans['history']
    hist.append({'player': player, 'kind': spell, 'magic': {spell: -1},})
    i = -2
    while (hist[i+1].get('kind', None) == 'counter') and (i > -len(hist)):
        hist[i]['countered'] = not hist[i].get('countered', False)
        i -= 1

SPELLBOOK['counter'] = counter


