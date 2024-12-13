"""Find an optimized configuration for the ASIC."""
import sys
from os import getcwd
from os.path import join, exists
import csv
sys.path.append(getcwd())
from measurements import read_asic as r_a # pylint: disable=wrong-import-position
from measurements import meas_helper as m_h # pylint: disable=wrong-import-position

CHIP = 1 # Chip number under test
TEMP = 20 # Experiment temperature
SUPPLY = 1.0 # Experiment voltage
VERBOSE = True # Verbose
MAX_CON = 2**16 # Max configuration
VDL0_BOUND = 1 # VDL0 faster (0) / slower (1) than VDL1

NB_CAN = 100 # Number of candidates
NB_MOD = 10 # Number of model points
MOD_DEG = 2 # Model complexity
F_NOISE = 30e-15 # F_NOISE parameter 30e-15
ALPHA = 1.0 # ALPHA parameter 1.94
BETA = 0.1 # BETA parameter
MIN_VDL_FREQ = 4e9 # Min VDL frequency
MAX_VDL_FREQ = 6e9#5.5e9 # Max VDL frequency
MAX_PER = 2000e-12 # Max DC/VDL period
MAX_CHECK = 100 # Max candidates check

file_index = 0 # pylint: disable=invalid-name
file_exist = True # pylint: disable=invalid-name
while file_exist:
    file_name = join('measurements', 'm6', f'm6_chip{CHIP:d}_temp{TEMP:d}_'
                     f'sup{SUPPLY:3.1f}_{file_index}.csv')
    file_index += 1
    file_exist = exists(file_name) # pylint: disable=invalid-name
with open(file_name, 'w', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(['confDC0 [-]', 'confDC1 [-]', 'confVDL0 [-]', 'confVDL1 [-]',
                     'perDC0 [ps]', 'perDC1 [ps]', 'perVDL0 [ps]', 'perVDL1 [ps]'])

reader = r_a.AsicReader()
reader.set_period_length(7, True)
reader.set_period_length(7, False)
reader.reset_asic(True, True)

helper = m_h.MeasHelper(chip=CHIP)
helper.build_model(nb_model_points=NB_MOD, model_degree=MOD_DEG, verbose=False)
calc = m_h.BoundCalc(f_noise=F_NOISE, alpha=ALPHA, beta=BETA,
                     min_vdl_freq=MIN_VDL_FREQ, max_vdl_freq=MAX_VDL_FREQ, verbose=False)

# Search for DC1:
bound_dc_1 = calc.get_p_dc1_bounds()
conf_dc_1s, per_dc_1s = helper.get_conf_model(1, bound_dc_1[0] * 1e12, bound_dc_1[1] * 1e12,
                                              nb_confs=NB_CAN, max_check=MAX_CHECK, verbose=VERBOSE)
if VERBOSE:
    print(f'PDC1 bounds: [{bound_dc_1[0] * 1e12:6.2f}, {bound_dc_1[1] * 1e12:6.2f}]')
    if len(conf_dc_1s) < NB_CAN: # type: ignore
        print(f'Failed to find {NB_CAN} candidates for DC1! '
              f'Only found {len(conf_dc_1s)}') # type: ignore
    else:
        print(f'Found {len(conf_dc_1s)} candidates for DC1!') # type: ignore
if len(conf_dc_1s) == 0: # type: ignore
    if VERBOSE:
        print('No DC1 candidates found!')
        print('Stopping script...')
    sys.exit()

# Search for DC0:
assert isinstance(conf_dc_1s, list)
conf_dc_0s = [None] * len(conf_dc_1s)
per_dc_0s = [None] * len(conf_dc_1s)
for i, p_i in enumerate(conf_dc_1s):
    bound_dc_0 = calc.get_p_dc_0_bounds(p_i * 1e-12)
    conf_dc_0s[i], per_dc_0s[i] = helper.get_conf_model(0, bound_dc_0[0] * 1e12, # type: ignore
                                                        bound_dc_0[1] * 1e12, nb_confs=1,
                                                        max_check=MAX_CHECK, verbose=False,
                                                        nb_confs_try=1)
    if VERBOSE:
        if conf_dc_0s[i] is not None:
            print(f'PDC0 bounds: [{bound_dc_0[0] * 1e12:6.2f}, {bound_dc_0[1]*1e12:6.2f}]')
            print(f'Collected {sum((1 for x in conf_dc_0s if x is not None))} confs', end='\r')
num = 0 # pylint: disable=invalid-name
assert isinstance(conf_dc_0s, list)
for c_i in conf_dc_0s:
    if c_i is not None:
        num += 1
if num == 0:
    if VERBOSE:
        print('No DC0 candidates found!')
        print('Stopping script...')
    sys.exit()
if VERBOSE:
    print(f'Found {num}/{NB_CAN} candidates for DC0/DC1 ({num / NB_CAN * 100} %)')

# Delete failed configurations:
assert isinstance(per_dc_1s, list)
for i in range(len(conf_dc_1s)-1, -1, -1):
    if conf_dc_0s[i] is None:
        del conf_dc_1s[i]
        del per_dc_1s[i]
        del conf_dc_0s[i]
        del per_dc_0s[i]

if VERBOSE:
    print('DC configurations so far:')
    for i, c_i in enumerate(conf_dc_0s):
        print(f'{i}: {c_i:05d} {per_dc_0s[i]:6.2f} | {conf_dc_1s[i]:05d} {per_dc_1s[i]:6.2f}')

# Search for VDL1:
bound_vdl_1 = calc.get_p_vdl_1_bounds()
print(f'PVDL1 bounds: {bound_vdl_1}')
conf_vdl_1s, per_vdl_1s = helper.get_conf_model(3, bound_vdl_1[0]*1e12, bound_vdl_1[1]*1e12,
                                                nb_confs=len(conf_dc_1s), max_check=MAX_CHECK,
                                                verbose=VERBOSE,
                                                other_confs=[0, 0, 127 * 256 + 255, 0])
assert isinstance(conf_vdl_1s, list)
assert isinstance(per_vdl_1s, list)
conf_vdl_1s = conf_vdl_1s[:len(conf_dc_1s)]
per_vdl_1s = per_vdl_1s[:len(conf_dc_1s)]
if conf_vdl_1s is None:
    if VERBOSE:
        print('No VDL1 candidates found!')
        print('Stopping script...')
    sys.exit()
if VERBOSE:
    print(f'PVDL1 bounds: [{bound_vdl_1[0] * 1e12:6.2f}, {bound_vdl_1[1] * 1e12:6.2f}]')
    if len(conf_vdl_1s) < len(conf_dc_1s):
        print(f'Failed to find {len(conf_dc_1s)} candidates for VDL1! '
              f'Only found {len(conf_vdl_1s)}')
    else:
        print(f'Found {len(conf_vdl_1s)} candidates for VDL1!')
if len(conf_vdl_1s) == 0:
    if VERBOSE:
        print('No VDL1 candidates found!')
        print('Stopping script...')
    sys.exit()

# Search for VDL0:
conf_vdl_0s = [None] * len(conf_vdl_1s)
per_vdl_0s = [None] * len(conf_vdl_1s)
for i in range(min(len(conf_vdl_1s), len(per_dc_1s))):
    bound_vdl_0 = calc.get_p_vdl_0_bounds(per_vdl_1s[i] * 1e-12,
                                          per_dc_1s[i] * 1e-12)[VDL0_BOUND]
    conf_vdl_0s[i], per_vdl_0s[i] = helper.get_conf_model(2, bound_vdl_0[0]*1e12, # type: ignore
                                                          bound_vdl_0[1] * 1e12,
                                                          nb_confs=1, max_check=MAX_CHECK,
                                                          verbose=False, nb_confs_try=1)
    if VERBOSE:
        print(f'PVDL0 bounds: [{bound_vdl_0[0] * 1e12:6.2f}, {bound_vdl_0[1] * 1e12:6.2f}]')
        if conf_vdl_0s[i] is not None:
            print(f'Collected {sum((1 for x in conf_vdl_0s if x is not None))} confs', end='\r')
num = 0 # pylint: disable=invalid-name
for i in range(min(len(conf_vdl_0s), len(conf_dc_0s))):
    if conf_dc_0s[i] is not None:
        num += 1
if num == 0:
    if VERBOSE:
        print('No VDL0 candidates found!')
        print('Stopping script...')
    sys.exit()
if VERBOSE:
    print(f'Found {num}/{len(conf_vdl_1s)} candidates for VDL0/VDL1 '
          f'({num / len(conf_vdl_1s) * 100} %)')

# Delete failed configurations:
conf_dc_0s = conf_dc_0s[:len(conf_vdl_1s)]
per_dc_0s = per_dc_0s[:len(conf_vdl_1s)]
conf_dc_1s = conf_dc_1s[:len(conf_vdl_1s)]
per_dc_1s = per_dc_1s[:len(conf_vdl_1s)]
for i in range(len(conf_vdl_0s) - 1, -1, -1):
    if conf_vdl_0s[i] is None:
        del conf_vdl_0s[i]
        del per_vdl_0s[i]
        del conf_vdl_1s[i]
        del per_vdl_1s[i]
        del conf_dc_0s[i]
        del per_dc_0s[i]
        del conf_dc_1s[i]
        del per_dc_1s[i]

if VERBOSE:
    print('VDL configurations so far:')
    for i, c_i in enumerate(conf_vdl_0s):
        print(f'{i}: {c_i:05d} {per_vdl_0s[i]:6.2f} | {conf_vdl_1s[i]:05d} {per_vdl_1s[i]:6.2f}')

# Check all configurations together:
if VERBOSE:
    print('One more last check for the candidates')
can_good = [False] * len(conf_dc_0s)
for i, c_i in enumerate(conf_dc_0s):
    other_confs = [c_i, conf_dc_1s[i], conf_vdl_0s[i], conf_vdl_1s[i]]
    a_dc_0 = helper.read_per(0, conf_dc_0s[i], other_confs==other_confs) # type: ignore
    a_dc_1 = helper.read_per(1, conf_dc_1s[i], other_confs=other_confs) # type: ignore
    a_vdl_0 = helper.read_per(2, conf_vdl_0s[i], other_confs=other_confs) # type: ignore
    a_vdl_1 = helper.read_per(3, conf_vdl_1s[i], other_confs=other_confs) # type: ignore
    if a_dc_0 is None:
        continue
    if a_dc_1 is None:
        continue
    if a_vdl_0 is None:
        continue
    if a_vdl_1 is None:
        continue
    if VERBOSE:
        print(f'Candidate [{i}/{len(conf_dc_0s)}] {per_dc_0s[i]:6.2f} {a_dc_0:6.2f} '
              f'| {per_dc_1s[i]:6.2f} {a_dc_1:6.2f} | {per_vdl_0s[i]:6.2f} {a_vdl_0:6.2f} '
              f'| {per_vdl_1s[i]:6.2f} {a_vdl_1:6.2f}')

    bound_dc_0 = calc.get_p_dc_0_bounds(a_dc_1 * 1e-12)
    if (bound_dc_0[0] >= a_dc_0 * 1e-12) | (bound_dc_0[1] <= a_dc_0 * 1e-12):
        if VERBOSE:
            print(f'Candidate [{i}/{len(conf_dc_0s)}] not good (DC0 failed: '
                  f'{a_dc_0:6.2f} [{bound_dc_0[0] * 1e12:6.2f}, {bound_dc_0[1] * 1e12:6.2f}])')
        continue
    bound_dc_1 = calc.get_p_dc1_bounds()
    if (bound_dc_1[0] >= a_dc_1 * 1e-12) | (bound_dc_1[1] <= a_dc_1 * 1e-12):
        if VERBOSE:
            print(f'Candidate [{i}/{len(conf_dc_0s)}] not good (DC1 failed: '
                  f'{a_dc_1:6.2f} [{bound_dc_1[0] * 1e12:6.2f}, {bound_dc_1[1] * 1e12:6.2f}])')
        continue
    bound_vdl_0 = calc.get_p_vdl_0_bounds(a_vdl_1 * 1e-12, a_dc_1 * 1e-12)[VDL0_BOUND]
    if (bound_vdl_0[0] >= a_vdl_0 * 1e-12) | (bound_vdl_0[1] <= a_vdl_0 * 1e-12):
        if VERBOSE:
            print(f'Candidate [{i}/{len(conf_dc_0s)}] not good (VDL0 failed: '
                  f'{a_vdl_0:6.2f} [{bound_vdl_0[0] * 1e12:6.2f}, {bound_vdl_0[1] * 1e12:6.2f}])')
        continue
    bound_vdl_1 = calc.get_p_vdl_1_bounds()
    if (bound_vdl_1[0] >= a_vdl_1 * 1e-12) | (bound_vdl_1[1] <= a_vdl_1 * 1e-12):
        if VERBOSE:
            print(f'Candidate [{i}/{len(conf_dc_0s)}] not good (VDL1 failed: '
                  f'{a_vdl_1:6.2f} [{bound_vdl_1[0] * 1e12:6.2f}, {bound_vdl_1[1] * 1e12:6.2f}])')
        continue
    can_good[i] = True
    per_dc_0s[i] = a_dc_0 # type: ignore
    per_dc_1s[i] = a_dc_1
    per_vdl_0s[i] = a_vdl_0 # type: ignore
    per_vdl_1s[i] = a_vdl_1
    if VERBOSE:
        print(f'Candidate [{i}/{len(conf_dc_0s)}] good')
for i in range(len(conf_dc_0s) -1, -1, -1):
    if not can_good[i]:
        del conf_vdl_0s[i]
        del per_vdl_0s[i]
        del conf_vdl_1s[i]
        del per_vdl_1s[i]
        del conf_dc_0s[i]
        del per_dc_0s[i]
        del conf_dc_1s[i]
        del per_dc_1s[i]
if VERBOSE:
    print('Finished candidate check, '
          f'{len(conf_dc_0s)}/{NB_CAN} ({len(conf_dc_0s) / NB_CAN * 100} %) found')
    print('Candidate confs:')
    print('| i  | DC0   | DC1   | VDL0  | VDL1  |')
    for i, c_i in enumerate(conf_dc_0s):
        c_dc_0 = f'{conf_dc_0s[i]:05d}'
        c_dc_1 = f'{conf_dc_1s[i]:05d}'
        c_vdl_0 = f'{conf_vdl_0s[i]:05d}'
        c_vdl_1 = f'{conf_vdl_1s[i]:05d}'
        print(f'| {i:02d} | {c_dc_0} | {c_dc_1} | {c_vdl_0} | {c_vdl_1} |')
if len(conf_dc_1s) == 0:
    if VERBOSE:
        print('No candidates remain, stopping script...')
    sys.exit()

# Store candidates:
with open(file_name, 'a', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    for i, c_i in enumerate(conf_dc_0s):
        writer.writerow([f'{c_i:05d}', f'{conf_dc_1s[i]:05d}', f'{conf_vdl_0s[i]:05d}',
                         f'{conf_vdl_1s[i]:05d}', f'{per_dc_0s[i]:6.2f}', f'{per_dc_1s[i]:6.2f}',
                         f'{per_vdl_0s[i]:6.2f}', f'{per_vdl_1s[i]:6.2f}'])
