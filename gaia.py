from __future__ import print_function

import numpy as np

import grimoire
from utils import inventories

def drop(trans):
    """Drops magic cones, maybe."""
    spells = list(grimoire.SPELLBOOK.keys())
    nspells = len(spells)
    hist = trans['history']
    invs = inventories(trans)
    for player, inv in invs.items():
        p = np.random.rand()
        cones = inv['cones']
        if (cones <= 512 and p <= cones / 1024.0) or \
           (cones > 512 and p <= cones / 2.0**(int(np.log2(cones)) + 2)):
            hist.append({'player': player, 'kind': 'drop', 
                         'magic': {spells[np.random.randint(0, nspells)]: 1}})
