"""Independently recompute the teaching models in the Weeks 8-12 notes.

These checks enumerate small circuits and use explicit SI conversions. They
do not claim a local synthesis, OpenSTA, OpenROAD, or foundry-signoff run.
"""
from itertools import product
from pathlib import Path
from math import isclose
import json, hashlib

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
results = {}

def close(actual, expected):
    assert isclose(actual, expected, rel_tol=1e-10, abs_tol=1e-16), (actual, expected)

def gate_arrival(delay, *arrivals):
    return max(arrivals) + delay

vectors = list(product((0, 1), repeat=3))
for a, b, c in vectors:
    assert (not ((a and b) or c)) == ((not a or not b) and not c)
    assert ((a and b) or c) == ((a or c) if b else c)
results['De Morgan and Shannon'] = {'assignments_each': len(vectors)}

original = gate_arrival(50, gate_arrival(50, gate_arrival(50, 40, 70), 20), 30)
reordered = gate_arrival(50, gate_arrival(50, gate_arrival(50, 20, 30), 40), 70)
balanced = gate_arrival(50, gate_arrival(50, 20, 30), gate_arrival(50, 40, 70))
assert (original, reordered, balanced) == (220, 180, 170)
direct = gate_arrival(20, gate_arrival(25, 30, 100), 40)
shannon = gate_arrival(30, gate_arrival(20, 30, 40), 40, 100)
assert (direct, shannon) == (145, 130)
assert max(500 + 50, 400 + 50, 400) == 550
assert max(500, 400, 50 + 400) == 500
assert 400 + 30 - 20 == 410
assert 2000 - 410 == 1590
assert (1000 - 5) - (5 + 80) == 910
results['Timing transformations and output constraint'] = {
    'AND_chain_ps': [original, reordered, balanced],
    'Shannon_ps': [direct, shannon], 'tutorial_slack_ps': 910}

def d03(a, b, c, d, e, fault=None):
    y = a and b
    u = y and not c if fault is None else fault
    return (not (y or u)) and (not (u or d)) and e

detected_sa1 = []
for v in product((0, 1), repeat=5):
    a, b, c, d, e = v
    assert d03(*v) == (not (a and b) and not d and e)
    assert d03(*v) == d03(*v, fault=0)
    if d03(*v) != d03(*v, fault=1):
        detected_sa1.append(v)
assert len(detected_sa1) == 6

def notebook_top(a, b, c, d, fault=None):
    g2 = not (a or b)
    g3 = not ((not b) or c) if fault is None else fault
    g4 = c or d
    return g2 and g3, g3 or g4

top_detect = []
for v in product((0, 1), repeat=4):
    good = notebook_top(*v)
    bad = notebook_top(*v, fault=0)
    assert good[0] == bad[0] == 0
    if good[1] != bad[1]:
        top_detect.append(v)
assert top_detect == [(0, 1, 0, 0), (1, 1, 0, 0)]
for a, b, c in vectors:
    g2 = not ((not a) and b)
    good_g3 = b and c
    bad_g3 = c  # Only the G3 input branch is stuck at one.
    good = not (g2 or good_g3)
    bad = not (g2 or bad_g3)
    assert good == bad == (not a and b and not c)

def d04(a, b, c, d, fault=None):
    branch = not (a and b) if fault is None else fault
    side = not (c or d)
    return not (branch and side)

d04_detect = [v for v in product((0, 1), repeat=4)
              if d04(*v) != d04(*v, fault=1)]
assert d04_detect == [(1, 1, 0, 0)]
results['Fault activation and redundancy'] = {
    'D03_assignments': 32, 'D03_sa0_redundant': True,
    'D03_sa1_detecting_vectors': len(detected_sa1),
    'notebook_top_detecting_vectors': top_detect,
    'notebook_bottom_branch_sa1_redundant': True,
    'D04_complete_vector': d04_detect[0]}

def shift(state, incoming):
    return incoming, state[0], state[1]

q = (0, 0, 0)
trace = [q]
for bit in (1, 0, 1):
    q = shift(q, bit)
    trace.append(q)
assert trace == [(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 0, 1)]
q = (0, 0, 0)
for bit in (0, 1, 1):
    q = shift(q, bit)
assert q == (1, 1, 0)
assert 1000 * (500 + 1) == 501000
assert 1000 * (2 * 500 + 1) == 1001000

def lfsr(q):
    return q[1], q[2], q[0] ^ q[1]

q = (0, 0, 1)
orbit = []
while q not in orbit:
    orbit.append(q)
    q = lfsr(q)
assert q == orbit[0] and len(orbit) == 7
assert [''.join(map(str, state)) for state in orbit] == [
    '001', '010', '101', '011', '111', '110', '100']
assert lfsr((0, 0, 0)) == (0, 0, 0)
assert set(orbit) == set(vectors) - {(0, 0, 0)}
assert round(100 * (31 / 32) ** 100, 2) == 4.18
assert round(100 * (31 / 32) ** 200, 3) == 0.175
results['Scan and BIST'] = {'shift_trace': trace,
    'LFSR_nonzero_period': len(orbit),
    'random_OR_fault_miss_100': (31 / 32) ** 100,
    'random_OR_fault_miss_200': (31 / 32) ** 200}

close((0.6 / 1.2) ** 2 * (0.6 / 1.2), 1 / 8)
close((1 / 8) * (20 / 10), 1 / 4)
close(1e-12 * 1 ** 2 * 1e9, 1e-3)
close((1 + 2) / 2, 1.5)
close(2e-8 * 100e-6 / (0.2e-6 * 0.4e-6), 25)
close(5e-15 * 1 / (20e-15 + 5e-15), 0.2)
close(0.05 * 0.4, 0.02)
close(0.02 / 0.8, 0.025)
close(100e-12 * 0.1 / 1e-9, 0.01)
close(10e-3 * 100e-12 / 20e-3, 50e-12)
close(0.2 / (10e-6 * 2e-6) / 1e4, 1e6)  # A/m² -> A/cm²
close(4500 / (10000 - 2000 - 500), 0.6)
close(2 - 0.1 - 0.1 - 0.2 - 0.3, 0.7 + 0.6)
results['Power and physical SI models'] = {'DVFS_power_ratio': 0.125,
    'DVFS_dynamic_energy_ratio': 0.25, 'wire_resistance_ohm': 25,
    'IR_drop_V': 0.02, 'decap_F': 50e-12, 'example_current_density_A_cm2': 1e6}

pins = [(1, 1), (4, 3), (6, 7), (6, 2)]
hpwl = max(x for x, y in pins) - min(x for x, y in pins)
hpwl += max(y for x, y in pins) - min(y for x, y in pins)
assert hpwl == 11
assert [max(0, use - 6) for use in (4, 5, 8)] == [0, 0, 2]
assert 4 * 80 - (80 + 30 + 80) == 130

def setup_bound(launch, capture, data, overhead=0):
    return launch + data + overhead - capture

assert max(setup_bound(50, 50, 200), setup_bound(50, 50, 300)) == 300
assert max(setup_bound(100, 50, 200), setup_bound(50, 100, 300)) == 250
assert max(setup_bound(100, 50, 200, 45), setup_bound(50, 100, 300, 45)) == 295
assert 50 + 15 + 20 - (100 + 10 + 5) == -30
assert 50 + 15 + 20 - (50 + 10 + 5) == 20
results['Placement and clock scheduling'] = {'HPWL_units': hpwl,
    'useful_skew_periods_ps': [300, 250, 295],
    'short_path_hold_slacks_ps': [20, -30]}

source_hashes = {str(day): hashlib.sha256(
    (ROOT/'Daily Notes'/f'Day {day:02d}.md').read_bytes()).hexdigest()
    for day in range(6, 10)}
qa = ROOT/'Resources/tools/pdf/qa'
qa.mkdir(parents=True, exist_ok=True)
(qa/'wrapup-example-checks.json').write_text(json.dumps({
    'results': results, 'source_sha256': source_hashes,
    'scope': 'Explicit teaching models; no new local ASIC-flow execution.'},
    indent=2), encoding='utf-8')
print('PASS: exhaustive fault/Boolean checks, scan bit ordering, seven-state LFSR, '
      'timing transformations, useful-skew/hold arithmetic, DVFS, wire RC and PDN units.')
