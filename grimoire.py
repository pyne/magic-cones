from __future__ import print_function
from collections import OrderedDict

import numpy as np

from utils import CONES_PER_SAPLING, CONES_PER_TREE, inventories, gross_cones

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
    _common_cone(CONES_PER_SAPLING, trans, player, spell, target=target)

SPELLBOOK['sapling'] = sapling

def tree(trans, player, spell, target=None):
    """adds a tree to a player (default) or target (optional)."""
    _common_cone(CONES_PER_TREE, trans, player, spell, target=target)

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

KOANS = [
'Ummon inquired of his monks, "This world is such a wide world! Why then do you answer to a temple bell and don ceremonial robes?',
"""A monk asked Ummon, "What is the Dharma Kaya (the ultimate formless timeless reality)?".
Ummon replied: "A garden of medicinal flowers."
The monk then said, "Is that all I need to understand?"
Ummon replied: "If that isn't enough, then you'll need to see the mythical Golden-Haired Lion."
""", 
"""A monk once asked Ummon, "What is the Dharma Kaya?"
Ummon answered: "The Six Ungraspables." (The Graspables are the five senses and the mind.[1])""",
"""When Ummon was asked "What is the pure Dharmakaya?", he replied: "The flowering hedge" (surrounding the privy).""",
"""Ummon Zenji said: "Men of immeasurable greatness are tossed about in the ebb and flow of words."
""",
"""Of the Zen saying: "Buddha preached for forty-nine years, but his tongue never moved," the master Gensha said:

"Pious teachers say that Buddhism helps us in every possible way, but think: how can it help the blind, the deaf, or the dumb? The blind cannot see the teacher's staff that is raised before them. The deaf cannot hear the teacher's words, no matter how wise. The dumb cannot ask their questions or speak their understanding. So since we cannot help these people, how can we say Buddhism helps in every possible way? What good is it?"
Many years later a monk asked the master Ummon to explain these words of Gensha. After making the questioner prostrate himself and then rise, Ummon swiped at him with his staff. The monk jumped back.
"Ah-ha!" said Ummon, "I see you are not blind!" Then he told the monk to come forward, which he did.
"Ah-ha!" said Ummon, "I see you are not deaf!" Then he asked the monk if he understood what all this to-do was about. The monk said he did not. "Ah-ha!" said Ummon, "I see you are not dumb!"
""",
"""A Zen student told Ummon- "Brilliancy of Buddha illuminates the whole universe."
Before he finished the phrase, Ummon asked: "You are reciting another's poem, are you not?"
"Yes", answered the student.
"You are sidetracked," said Ummon.
Afterwards another teacher, Shishin, asked his pupils: "At which point did that student go off the track?"
""",
"""Tozan (Ummon's future successor as head of the Ummon school) went to Ummon. Ummon asked him where he came from. Tozan said, "From Sato Village."
Ummon asked: "In what temple did you remain for the summer?"
Tozan replied, "The temple of Hoji, south of the lake."
"When did you leave there?" asked Ummon, wondering how long Tozan would continue with such factual answers.
"The twenty-fifth of August", answered Tozan.
Ummon then said: "I should give you three blows, but today I forgive you."
The next day Tozan bowed to Ummon and asked, "Yesterday you forgave me three blows. I do not know why you thought me wrong." Ummon, rebuking Tozan's spiritless responses, said: "You are good for nothing! You simply wander from one monastery to another." Before Ummon's words were ended, Tozan was enlightened.""",
"""Once Hsueh-feng came before the assembly and said, "In a southern mountain, there is a turtle-nosed serpent. You monks must have a good look at this creature." Ch'ang-ch'ing, Yun-men, and Hsuan-sha were in the assembly. Ch'ang-ch'ing stepped forward and said: "In this hall someone will lose his body and life today." Yun-men threw his staff down in front of Hsueh-feng and made a gesture as of fear at discovering the serpent. Hsuan-sha said, "Brother Ch'ang-ch'ing's answer has some substance to it. However, I should not say it thus, but ask why we refer to the southern mountain."
""",
"""Ummon asked the head monk, "What sutra are you lecturing on?"
"The Nirvana Sutra."
"The Nirvana Sutra has the Four Virtues, hasn't it?"
"It has."
Ummon asked, picking up a cup, "How many virtues has this?"
"None at all, " said the monk.
"But ancient people said it had, didn't they?" said Ummon. "What do you think of what they said?" Ummon struck the cup and asked, "You understand?"
"No," said the monk.
"Then," said Ummon, "You'd better go on with your lectures on the sutra."
""",
"""Suigan, at the end of the annual summer meditation retreat, said to his monks, "The whole summer have I lectured you. Look! Has Suigan any eybrows?" Hofuku said: "A robber knows in his heart he is a thief." Chokei said, "Far from dropping off from too much talking, they have grown longer!" But then Ummon forcefully shouted "Kan!"
""",
"""Monk: "What is the one road of Ummon?"
Ummon: "Personal Experience!"
Monk: "What is the Way?"
Ummon: ""Go!"
Monk: "What is the road, where is the Way?"
Ummon: "Begin walking it!"
""",
"""A monk asked Ummon, "What will happen when the leaves fall and the trees become bare?" Ummon said, "Golden Wind!" (or, "The trunk is visible in the autumn wind.")""",
"""Ummon once lived within a temple called the "Chapel of Holy Fruits". One morning, a government official visited him, and asked him, "Are your fruits well-ripened now?" "None of them has ever been called green", replied Ummon.""",
"""A travelling monk asked Ummon, "What is the teaching given by Gautama Buddha during his lifetime?" Ummon replied: "The teaching confronts each."
""",
"""A monk asked Ummon. "What would the Shakyamuni Buddha have said if there were no one to hear and no occasion to teach?" Ummon answered: "The opposite of statement."
""",
"""One day Ummon stood up and said to his disciples: "If you do not see a man for three days, do not think he is the same man. How about you?" No one spoke, so he said: "One thousand!"
""",
"""A monk asked Ummon, "What is the kind of talk that transcends Buddhas and Patriarchs?" Ummon replied: "Rice cake!"
""",
"""A monk asked Ummon, "What is your family tradition?" Ummon replied thus: "Oh, it looks like students who wish to come to learn are already outside the gate."
""",
"""A monk asked Ummon, "What is Ummon's melody?" Ummon replied: "The twenty-fifth of December!"
""",
"""A monk asked Ummon, "What is the samadhi of each individual thing?" Ummon replied: "Rice in bowl, water in pail!"
""",
"""A monk asked Ummon, "No thoughts have risen. Are there any faults or not?" Ummon said: "Mount Sumeru!"
""",
"""Said Ummon to his disciples, "I do not ask you to say anything about before the fifteenth day of the month, but say something about after the fifteenth day of the month." Because no monk could reply, Ummon answered himself and said, "Every day is a good day!"
""",
"""Said Ummon to his disciples, "However wonderful a thing is, it may be that it is better not to have it at all."
""",
"""A monk asked Kenpo, "The one road of Nirvana leads into the ten quarters. But where does it begin?" Kenpo raised his staff and traced a horizontal line in the air. "Here." Disappointed, the monk went to Ummon and asked him the same question. Ummon held up his fan, and said: "This fan leaps up to the 33rd heaven and hits the presiding deity on the nose, then it dives down into the Eastern Sea where it hits the holy carp. The carp becomes a dragon which then brings a flood of rain."
""",
"""One day, while lecturing his monks, Ummon asked them, "Do you want to meet the old Patriarchs?" Before any of the monks could answer, he pointed his stick above their heads and said, "The Patriarchs are jumping on your head!" Then he asked, "Do you wish to look them in the eye?" He pointed to the ground and said: "They are all under our feet!" After a moment, he spoke to himself, saying: "I made a great feast in the joss house, but the hungry gods are never satisfied."
""",
"""A monk once asked Ummon, "What is this place where knowledge is useless?" Ummon answered him: "Knowledge and emotion cannot fathom it!"
""",
"""Yun-men asked: "If a person who is difficult to change should come to you, would you receive him?"
The master answered: "Ts'ao-shan has no such leisure."
Monk: "Where is the place from which all buddhas come?"
Yun-men: "Next question, please!"
""",
]

def koan(trans, player, spell, target=None):
    """grants wisdom. A duck!"""
    hist = trans['history']
    hist.append({'player': player, 'kind': spell, 'magic': {spell: -1},})
    k = KOANS[np.random.randint(0, len(KOANS))]
    print(k.strip())

SPELLBOOK['koan'] = koan

def spruce(trans, player, spell, target=None):
    """receive a cone for every line of style guide fixes. Target is a 
    comma-separated string of a pull request number and number of lines, 
    for example '42,10'. Capped at 1/4 of the world's e-cone-omy.
    """
    hist = trans['history']
    pr, n = tuple(map(int, target.split(',')))
    n = min(n, int(gross_cones(trans)/4.0))
    hist.append({'player': player, 'kind': spell, 'pr': pr, 'magic': {spell: -1},
                 'cones': n})

SPELLBOOK['spruce'] = spruce

def slash(trans, player, spell, target=None):
    """receive a cone for every net line of code removed. Target is a 
    comma-separated string of a pull request number and number of lines 
    removed, for example '42,10'. Capped at 1/4 of the world's e-cone-omy.
    """
    hist = trans['history']
    pr, n = tuple(map(int, target.split(',')))
    n = min(n, int(gross_cones(trans)/4.0))
    hist.append({'player': player, 'kind': spell, 'pr': pr, 'magic': {spell: -1},
                 'cones': n})

SPELLBOOK['slash'] = slash

def cypress(trans, player, spell, target=None):
    """receive a cone for every line of documentation added. Target is a 
    comma-separated string of a pull request number and number of lines,
    for example '42,10'. Capped at 1/4 of the world's e-cone-omy.
    """
    hist = trans['history']
    pr, n = tuple(map(int, target.split(',')))
    n = min(n, int(gross_cones(trans)/4.0))
    hist.append({'player': player, 'kind': spell, 'pr': pr, 'magic': {spell: -1},
                 'cones': n})

SPELLBOOK['cypress'] = cypress

def sugar(trans, player, spell, target=None):
    """congratulate, thank, or otherwise say something nice to another player
    publicly and receive a sapling. 
    """
    hist = trans['history']
    hist.append({'player': player, 'kind': spell, 'magic': {spell: -1},
                 'cones': CONES_PER_SAPLING})

SPELLBOOK['sugar'] = sugar

def pitch(trans, player, spell, target=None):
    """publicly pitch the project to a potential user and receive a sapling."""
    hist = trans['history']
    hist.append({'player': player, 'kind': spell, 'magic': {spell: -1},
                 'cones': CONES_PER_SAPLING})

SPELLBOOK['pitch'] = pitch

def lodgepole(trans, player, spell, target=None):
    """report an issue and receive a sapling."""
    hist = trans['history']
    hist.append({'player': player, 'kind': spell, 'magic': {spell: -1},
                 'cones': CONES_PER_SAPLING})

SPELLBOOK['lodgepole'] = lodgepole

def larch(trans, player, spell, target=None):
    """triggers an extra drop ceremony."""
    hist = trans['history']
    hist.append({'player': player, 'kind': spell, 'magic': {spell: -1}})
    import gaia
    gaia.drop(trans)

SPELLBOOK['larch'] = larch

def redwood(trans, player, spell, target=None):
    """gives a sapling to every co-author of a conference proceeding.
    The proceeding must be accepted. Target a is comma-separated list
    of co-author player names.
    """
    hist = trans['history']
    coauthors = target.split(',')
    hist.append({'player': player, 'kind': spell, 'magic': {spell: -1}})
    for coauthor in coauthors:
        hist.append({'player': coauthor, 'kind': spell, 'cones': CONES_PER_SAPLING})

SPELLBOOK['redwood'] = redwood

def sequoia(trans, player, spell, target=None):
    """gives a tree to every co-author of a journal article.
    The article must be accepted. Target a is comma-separated list
    of co-author player names.
    """
    hist = trans['history']
    coauthors = target.split(',')
    hist.append({'player': player, 'kind': spell, 'magic': {spell: -1}})
    for coauthor in coauthors:
        hist.append({'player': coauthor, 'kind': spell, 'cones': CONES_PER_TREE})

SPELLBOOK['sequoia'] = sequoia

def chaos(trans, player, spell, target=None):
    """???"""
    hist = trans['history']
    hist.append({'player': player, 'kind': spell, 'magic': {spell: -1}})
    import gaia
    gaia.drop(trans)
    inv = inventories(trans)[player]
    tran = {'player': player, 'kind': spell, 'cones': -inv['cones'], 
            'magic': {key: -value for key, value in inv['magic'].items()}}
    magic_cone_worth = np.random.randint(0, CONES_PER_TREE+1)
    leyline = inv['cones'] + magic_cone_worth * sum(inv['magic'].values())
    leyline *= 1.5 * np.random.rand() + 0.5
    p = np.random.rand()
    tran['cones'] += int(p * leyline)
    spells = list(SPELLBOOK.keys())
    nspells = len(spells)
    for i in range(int(leyline * (1.0 - p) / magic_cone_worth)):
        key = spells[np.random.randint(0, nspells)]
        if key not in tran['magic']:
            tran['magic'][key] = 0
        tran['magic'][key] += 1
    hist.append(tran)
    for i in range(np.random.randint(0, 3)):
        gaia.drop(trans)

SPELLBOOK['chaos'] = chaos

