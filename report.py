from __future__ import print_function
from collections import namedtuple

from prettytable import PrettyTable

from utils import SAPLINGS_PER_CONE, TREES_PER_CONE, inventories

def report(trans, html=False):
    """Returns a summary report of all of the transactions."""
    invs = inventories(trans)
    rankings = []
    for player, inv in invs.items():
        rankings.append((player, inv['cones'], inv['magic']))
    rankings.sort(key=lambda x: x[1], reverse=True)
    listings = []
    for player, cones, magic in rankings:
        listings.append((player, 
                         cones // TREES_PER_CONE, 
                         cones // SAPLINGS_PER_CONE, 
                         cones % SAPLINGS_PER_CONE, 
                         ', '.join(['{1}x {0} cones'.format(key, value) for key, value \
                                    in sorted(magic.items()), if value > 0])
                         ))
    tab = PrettyTable(['Player', 'Trees', 'Saplings', 'Cones', 'Magic Cones'])
    for listing in listings:
        tab.add_row(listing)
    rep = tab.get_html_string() if html else tab.get_string()
    return rep