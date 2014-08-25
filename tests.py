from __future__ import print_function

from nose.tools import assert_equal, assert_in

import grimoire
import utils
import gaia

def test_decay():
    spell = 'chaos'
    hist = [{'player': 'a', 'cones': 1024},]
    trans = {'history': hist}
    gaia.decay(trans)
    exp = [{'player': 'a', 'kind': 'decay', 'cones': -13}, 
           {'player': 'a', 'kind': 'decay', 'cones': -14}]
    yield assert_in, hist[-1], exp

def test_cast_cone():
    hist = [{'player': 'a', 'cones': 0, 'magic': {'cone': 1}}]
    trans = {'history': hist}
    grimoire.cast(trans, 'a', 'cone')
    exp = {'player': 'a', 'cones': 1, 'kind': 'cone', 'magic': {'cone': -1}}
    yield assert_equal, exp, hist[-1]

    hist.append({'player': 'b', 'cones': 0, 'magic': {'cone': 1}})
    grimoire.cast(trans, 'b', 'cone', target='a')
    exp_b = {'player': 'b', 'cones': 0, 'kind': 'cone', 'magic': {'cone': -1}, 
             'target': 'a'}
    exp_a = {'player': 'a', 'cones': 1, 'kind': 'cone', 'target': 'b'}
    yield assert_equal, exp_b, hist[-2]
    yield assert_equal, exp_a, hist[-1]

def test_cast_sapling():
    spell = 'sapling'
    hist = [{'player': 'a', 'cones': 0, 'magic': {spell: 1}}]
    trans = {'history': hist}
    grimoire.cast(trans, 'a', spell)
    exp = {'player': 'a', 'cones': 8, 'kind': spell, 'magic': {spell: -1}}
    yield assert_equal, exp, hist[-1]

    hist.append({'player': 'b', 'cones': 0, 'magic': {'sapling': 1}})
    grimoire.cast(trans, 'b', spell, target='a')
    exp_b = {'player': 'b', 'cones': 0, 'kind': spell, 'magic': {spell: -1}, 
             'target': 'a'}
    exp_a = {'player': 'a', 'cones': 8, 'kind': spell, 'target': 'b'}
    yield assert_equal, exp_b, hist[-2]
    yield assert_equal, exp_a, hist[-1]

def test_cast_tree():
    spell = 'tree'
    hist = [{'player': 'a', 'cones': 0, 'magic': {spell: 1}}]
    trans = {'history': hist}
    grimoire.cast(trans, 'a', spell)
    exp = {'player': 'a', 'cones': 64, 'kind': spell, 'magic': {spell: -1}}
    yield assert_equal, exp, hist[-1]

    hist.append({'player': 'b', 'cones': 0, 'magic': {spell: 1}})
    grimoire.cast(trans, 'b', spell, target='a')
    exp_b = {'player': 'b', 'cones': 0, 'kind': spell, 'magic': {spell: -1}, 
             'target': 'a'}
    exp_a = {'player': 'a', 'cones': 64, 'kind': spell, 'target': 'b'}
    yield assert_equal, exp_b, hist[-2]
    yield assert_equal, exp_a, hist[-1]

def test_cast_counter():
    spell = 'counter'
    hist = [{'player': 'a', 'cones': 0, 'magic': {spell: 1}},
            {'player': 'b', 'cones': 0, 'magic': {spell: 1, 'cone': 1}}]
    trans = {'history': hist}

    # b gives self a cone
    grimoire.cast(trans, 'b', 'cone')
    invs = utils.inventories(trans)
    yield assert_equal, 1, invs['b']['cones']

    # a counters b
    grimoire.cast(trans, 'a', 'counter')
    invs = utils.inventories(trans)
    yield assert_equal, 0, invs['b']['cones']

    # b counters a's counter
    grimoire.cast(trans, 'b', 'counter')
    invs = utils.inventories(trans)
    yield assert_equal, 1, invs['b']['cones']

def test_cast_clone():
    spell = 'clone'
    hist = [{'player': 'a', 'cones': 0, 'magic': {spell: 1}},
            {'player': 'b', 'cones': 1, 'pr': 42}, 
            {'player': 'c', 'cones': 1, 'pr': 42}, 
            ]
    trans = {'history': hist}
    grimoire.cast(trans, 'a', spell, target='42')
    invs = utils.inventories(trans)
    yield assert_equal, 2, invs['a']['cones']

def test_cast_feed():
    spell = 'feed'
    hist = [{'player': 'a', 'cones': 100, 'magic': {spell: 1}}]
    trans = {'history': hist}
    grimoire.cast(trans, 'a', spell)
    exp = {'player': 'a', 'cones': 0, 'kind': spell, 'magic': {spell: -1}}
    yield assert_equal, exp, hist[-1]

    hist.append({'player': 'b', 'cones': 100, 'magic': {spell: 1}})
    grimoire.cast(trans, 'b', spell, target='a')
    exp_b = {'player': 'b', 'cones': -12, 'kind': spell, 'magic': {spell: -1}, 
             'target': 'a'}
    exp_a = {'player': 'a', 'cones': 12, 'kind': spell, 'target': 'b'}
    yield assert_equal, exp_b, hist[-2]
    yield assert_equal, exp_a, hist[-1]

def test_cast_cede():
    spell = 'cede'
    hist = [{'player': 'a', 'cones': 100, 'magic': {spell: 1}}]
    trans = {'history': hist}
    grimoire.cast(trans, 'a', spell)
    exp = {'player': 'a', 'cones': 0, 'kind': spell, 'magic': {spell: -1}}
    yield assert_equal, exp, hist[-1]

    hist.append({'player': 'b', 'cones': 100, 'magic': {spell: 1}})
    grimoire.cast(trans, 'b', spell, target='a')
    exp_b = {'player': 'b', 'cones': -25, 'kind': spell, 'magic': {spell: -1}, 
             'target': 'a'}
    exp_a = {'player': 'a', 'cones': 25, 'kind': spell, 'target': 'b'}
    yield assert_equal, exp_b, hist[-2]
    yield assert_equal, exp_a, hist[-1]

def test_cast_deed():
    spell = 'deed'
    hist = [{'player': 'a', 'cones': 100, 'magic': {spell: 1}}]
    trans = {'history': hist}
    grimoire.cast(trans, 'a', spell)
    exp = {'player': 'a', 'cones': 0, 'kind': spell, 'magic': {spell: -1}}
    yield assert_equal, exp, hist[-1]

    hist.append({'player': 'b', 'cones': 100, 'magic': {spell: 1}})
    grimoire.cast(trans, 'b', spell, target='a')
    exp_b = {'player': 'b', 'cones': -50, 'kind': spell, 'magic': {spell: -1}, 
             'target': 'a'}
    exp_a = {'player': 'a', 'cones': 50, 'kind': spell, 'target': 'b'}
    yield assert_equal, exp_b, hist[-2]
    yield assert_equal, exp_a, hist[-1]

def test_cast_meed():
    spell = 'meed'
    hist = [{'player': 'a', 'cones': 100, 'magic': {spell: 1}}]
    trans = {'history': hist}
    grimoire.cast(trans, 'a', spell)
    exp = {'player': 'a', 'cones': 0, 'kind': spell, 'magic': {spell: -1}}
    yield assert_equal, exp, hist[-1]

    hist.append({'player': 'b', 'cones': 100, 'magic': {spell: 1}})
    grimoire.cast(trans, 'b', spell, target='a')
    exp_b = {'player': 'b', 'cones': -100, 'kind': spell, 'magic': {spell: -1}, 
             'target': 'a'}
    exp_a = {'player': 'a', 'cones': 100, 'kind': spell, 'target': 'b'}
    yield assert_equal, exp_b, hist[-2]
    yield assert_equal, exp_a, hist[-1]

def test_cast_koan():
    spell = 'koan'
    hist = [{'player': 'a', 'cones': 0, 'magic': {spell: 1}}]
    trans = {'history': hist}
    grimoire.cast(trans, 'a', spell)
    exp = {'player': 'a', 'kind': spell, 'magic': {spell: -1}}
    yield assert_equal, exp, hist[-1]

def test_cast_spruce():
    spell = 'spruce'
    hist = [{'player': 'a', 'cones': 50, 'magic': {spell: 1}},]
    trans = {'history': hist}
    grimoire.cast(trans, 'a', spell, target='42,10')
    exp = {'player': 'a', 'kind': spell, 'pr': 42, 'magic': {spell: -1},
           'cones': 10}
    yield assert_equal, exp, hist[-1]
    invs = utils.inventories(trans)
    yield assert_equal, 60, invs['a']['cones']

def test_cast_slash():
    spell = 'slash'
    hist = [{'player': 'a', 'cones': 50, 'magic': {spell: 1}},]
    trans = {'history': hist}
    grimoire.cast(trans, 'a', spell, target='42,10')
    exp = {'player': 'a', 'kind': spell, 'pr': 42, 'magic': {spell: -1},
           'cones': 10}
    yield assert_equal, exp, hist[-1]
    invs = utils.inventories(trans)
    yield assert_equal, 60, invs['a']['cones']

def test_cast_cypress():
    spell = 'cypress'
    hist = [{'player': 'a', 'cones': 50, 'magic': {spell: 1}},]
    trans = {'history': hist}
    grimoire.cast(trans, 'a', spell, target='42,10')
    exp = {'player': 'a', 'kind': spell, 'pr': 42, 'magic': {spell: -1},
           'cones': 10}
    yield assert_equal, exp, hist[-1]
    invs = utils.inventories(trans)
    yield assert_equal, 60, invs['a']['cones']

def test_cast_sugar():
    spell = 'sugar'
    hist = [{'player': 'a', 'cones': 0, 'magic': {spell: 1}},]
    trans = {'history': hist}
    grimoire.cast(trans, 'a', spell)
    exp = {'player': 'a', 'kind': spell, 'magic': {spell: -1},
           'cones': 8}
    yield assert_equal, exp, hist[-1]

def test_cast_pitch():
    spell = 'pitch'
    hist = [{'player': 'a', 'cones': 0, 'magic': {spell: 1}},]
    trans = {'history': hist}
    grimoire.cast(trans, 'a', spell)
    exp = {'player': 'a', 'kind': spell, 'magic': {spell: -1},
           'cones': 8}
    yield assert_equal, exp, hist[-1]

def test_cast_lodgepole():
    spell = 'lodgepole'
    hist = [{'player': 'a', 'cones': 0, 'magic': {spell: 1}},]
    trans = {'history': hist}
    grimoire.cast(trans, 'a', spell)
    exp = {'player': 'a', 'kind': spell, 'magic': {spell: -1},
           'cones': 8}
    yield assert_equal, exp, hist[-1]

def test_cast_larch():
    spell = 'larch'
    hist = [{'player': 'a', 'cones': 0, 'magic': {spell: 1}},]
    trans = {'history': hist}
    grimoire.cast(trans, 'a', spell)
    exp = {'player': 'a', 'kind': spell, 'magic': {spell: -1}}
    yield assert_equal, exp, hist[1]

def test_cast_redwood():
    spell = 'redwood'
    hist = [{'player': 'a', 'cones': 0, 'magic': {spell: 1}},]
    trans = {'history': hist}
    grimoire.cast(trans, 'a', spell, target='b,c')
    exp_a = {'player': 'a', 'kind': spell, 'magic': {spell: -1}}
    yield assert_equal, exp_a, hist[-3]
    exp_b = {'player': 'b', 'kind': spell, 'cones': 8}
    yield assert_equal, exp_b, hist[-2]
    exp_c = {'player': 'c', 'kind': spell, 'cones': 8}
    yield assert_equal, exp_c, hist[-1]

def test_cast_sequoia():
    spell = 'sequoia'
    hist = [{'player': 'a', 'cones': 0, 'magic': {spell: 1}},]
    trans = {'history': hist}
    grimoire.cast(trans, 'a', spell, target='b,c')
    exp_a = {'player': 'a', 'kind': spell, 'magic': {spell: -1}}
    yield assert_equal, exp_a, hist[-3]
    exp_b = {'player': 'b', 'kind': spell, 'cones': 64}
    yield assert_equal, exp_b, hist[-2]
    exp_c = {'player': 'c', 'kind': spell, 'cones': 64}
    yield assert_equal, exp_c, hist[-1]

def test_cast_chaos():
    spell = 'chaos'
    hist = [{'player': 'a', 'cones': 1024, 'magic': {spell: 1}},]
    trans = {'history': hist}
    grimoire.cast(trans, 'a', spell)

