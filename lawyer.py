from __future__ import print_function
from inspect import getdoc

from prettytable import PrettyTable

import grimoire 

TEXT = """{intro}

basics
------
{basics}

grimoire
--------
{mceffects}

{mctable}"""

HTML = """{intro}

<h3>Basics</h3>
{basics}

<h3>Grimoire</h3>
{mceffects}
<br/><br/>
{mctable}
"""

INTRO = ('Magic Cones is a mystical game of conifers and collaboration. \n'
         'Build reputation, cast spells, grow the code base.')

BASICS_TEXT = """\
The purpose of Magic Cones is to improve software through reputation-based
incentives. The game is played via pull requests and the command line.

*Cones* are the primary currency. One cone is awarded for every pull request 
that a player open. A cone is also awarded if a player reviews or merges a 
pull request. No cones are awarded for self-merged pull requests or for unmerged
pull requests (either closed or open). Cones are tallied only after a merge.

Eight cones become a *sapling* and eight saplings become a *tree*.

A player who opens a pull request, the *requester*, may add a *bounty* to the 
pull request to encourage prompt review. This is done by adding the following
to the original pull request message:

    **Bounty** - N

Here N is replaced by the integer bounty value. Upon merge, the bounty value 
is transferred from the requester to the *merger* in addition to the normal cone 
awards. Other reviewers besides the merger do not receive the bounty.

Weekly, the Great Earth Mother shakes down her trees and rewards players in 
the sacred *drop* ceremony. During the drop, every player has the opportunity
to receive special *magic cones* that are infused with powerful life energies.
The magic cones may be *cast*, producing a boon to the *caster* or another 
*target* player. The exact effect depends on the kind of magic cone. The magic
cone may be cast at any time and is destroyed in the process.

The probability of receiving a magic cone during the weekly drop is proportional
to the player's *ley line of credit*, or the total number of trees, saplings, 
and mundane cones. If the ley line of credit is less than 512, then the 
likelihood is the ley line divided by 1024. If the ley line is greater than 512, 
then the likelihood is the ley line divided by 2^(int(log2(leyline)) + 2).
Every magic cone is equally probable to obtain."""

BASICS_HTML = """
The purpose of Magic Cones is to improve software through reputation-based
incentives. The game is played via pull requests and the command line.
<br/><br/>

<i>Cones</i> are the primary currency. One cone is awarded for every pull request 
that a player open. A cone is also awarded if a player reviews or merges a 
pull request. No cones are awarded for self-merged pull requests or for unmerged
pull requests (either closed or open). Cones are tallied only after a merge.
<br/><br/>

Eight cones become a <i>sapling</i> and eight saplings become a <i>tree</i>.
<br/><br/>

A player who opens a pull request, the <i>requester</i>, may add a <i>bounty</i> to the 
pull request to encourage prompt review. This is done by adding the following
to the original pull request message:
<br/><br/>

<p style="text-indent:50px;">
**Bounty** - N
</p>
<br/><br/>

Here N is replaced by the integer bounty value. Upon merge, the bounty value 
is transferred from the requester to the <i>merger</i> in addition to the normal cone 
awards. Other reviewers besides the merger do not receive the bounty.
<br/><br/>

Weekly, the Great Earth Mother shakes down her trees and rewards players in 
the sacred <i>drop</i> ceremony. During the drop, every player has the opportunity
to receive special <i>magic cones</i> that are infused with powerful life energies.
The magic cones may be <i>cast</i>, producing a boon to the <i>caster</i>  or another 
<i>target</i> player. The exact effect depends on the kind of magic cone. The magic
cone may be cast at any time and is destroyed in the process.
<br/><br/>

The probability of receiving a magic cone during the weekly drop is proportional
to the player's <i>ley line of credit</i>, or the total number of trees, saplings, 
and mundane cones. If the ley line of credit is less than 512, then the 
likelihood is the ley line divided by 1024. If the ley line is greater than 512, 
then the likelihood is the ley line divided by 2^(int(log2(leyline)) + 2).
Every magic cone is equally probable to obtain.
<br/><br/>
"""

MCEFFECTS = 'Magic cones have the following effects when cast:'

def rules(html=False):
    """Returns a string containing the Magic Cones rules."""
    mctab = PrettyTable(['Magic Cone', 'Spell'])
    mctab.border = False
    mctab.header = False
    mctab.align = 'l'
    for key, f in grimoire.SPELLBOOK.items():
        doc = getdoc(f)
        mctab.add_row((key, doc))
    p = {'intro': INTRO, 'mceffects': MCEFFECTS}
    if html:
        template = HTML 
        p['basics'] = BASICS_HTML
        p['mctable'] = mctab.get_html_string(format=True)
    else:
        template = TEXT
        p['basics'] = BASICS_TEXT
        p['mctable'] = mctab.get_string()
    s = template.format(**p)
    return s
