from __future__ import print_function
import io
import os

SAPLINGS_PER_CONE = 8
TREES_PER_CONE = 64

def inventories(trans):
    inventories = {}
    hist = trans['history']
    for tran in hist:
        kind = tran.get('kind', None)
        countered = tran.get('countered', False)
        inv = inventories.get(tran['player'], {'cones': 0, 'magic': {}})
        inventories[tran['player']] = inv
        inv['cones'] += 0 if countered else tran.get('cones', 0)
        if 'magic' not in inv:
            inv['magic'] = {}
        for key in tran.get('magic', ()):
            if countered and key != kind:
                continue
            inv['magic'][key] = tran['magic'][key] + inv['magic'].get(key, 0)
    return inventories

def newoverwrite(s, filename, verbose=False):
    """Useful for not forcing re-compiles and thus playing nicely with the
    build system.  This is acomplished by not writing the file if the existsing
    contents are exactly the same as what would be written out.

    Parameters
    ----------
    s : str
        string contents of file to possible
    filename : str
        Path to file.
    vebose : bool, optional
        prints extra message

    """
    if os.path.isfile(filename):
        with io.open(filename, 'rb') as f:
            old = f.read()
        if s == old:
            return
    else:
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname) and len(dirname) > 0:
            os.makedirs(dirname)
    with io.open(filename, 'wb') as f:
        f.write(s.encode())
    if verbose:
        print("  wrote " + filename)