from __future__ import print_function
import io
import os

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