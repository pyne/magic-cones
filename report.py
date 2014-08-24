from __future__ import print_function
from collections import namedtuple
from textwrap import TextWrapper

from prettytable import PrettyTable

from utils import CONES_PER_SAPLING, CONES_PER_TREE, inventories

def report(trans, html=False):
    """Returns a summary report of all of the transactions."""
    invs = inventories(trans)
    rankings = []
    for player, inv in invs.items():
        rankings.append((player, inv['cones'], inv['magic']))
    rankings.sort(key=lambda x: x[1], reverse=True)
    listings = []
    tw = TextWrapper(width=30)
    mctemp = '{1}x {0} cone{2}'
    for player, cones, magic in rankings:
        s = ', '.join([mctemp.format(key, value, '' if value == 1 else 's') \
                       for key, value in sorted(magic.items()) if value > 0])
        s = '\n'.join(tw.wrap(s))
        listings.append((player, 
                         cones // CONES_PER_TREE or '', 
                         cones // CONES_PER_SAPLING or \
                            ('' if cones // CONES_PER_TREE == 0 else 0), 
                         cones % CONES_PER_SAPLING,
                         s,
                         ))
    tab = PrettyTable(['Player', 'Trees', 'Saplings', 'Cones', 'Magic Cones'])
    for listing in listings:
        tab.add_row(listing)
    rep = tab.get_html_string(format=True) if html else tab.get_string()
    return rep