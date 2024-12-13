"""Measure jitter strength experiment."""
import sys
from os import getcwd
from os.path import join
import time
import csv
import numpy as np
import matplotlib.pyplot as plt
sys.path.append(getcwd())
from measurements import read_asic as r_a # pylint: disable=wrong-import-position

CHIP = 4
CONFS = ((0, 0, 0, 65376), (0, 0, 0, 65376), (12288, 12288, 0, 65376),
         (8192, 1, 0, 61567), (8192, 1, 0, 61671))

NB_SAMPLES = 2**16
NB_REPEATS = 100
VERBOSE = False

ns = [0, 1, 2, 3]
file_name = join('measurements', 'm5', f'm5_chip{CHIP:d}.csv')
with open(file_name, 'w', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',')
    csv_writer.writerow(['confDC0', 'confDC1', 'confVDL0', 'confVDL1', 'perDC0 [ps]',
                         'perDC1 [ps]', 'perVDL0 [ps]', 'perVDL1 [ps]', 'n', 'cntMean', 'cntVar'])

reader = r_a.AsicReader()
reader.set_period_length(7, True)
reader.set_period_length(7, False)

for ri in range(NB_REPEATS):
    ni = 0 # pylint: disable=invalid-name
    while ni < len(ns):
        n = ns[ni] # pylint: disable=invalid-name
        ro_pers = [0.0] * 4
        breaked = False # pylint: disable=invalid-name
        for ro_check in range(4):
            reader.set_conf(1, 0, CONFS[CHIP][0], CONFS[CHIP][1], 0, int(ro_check < 2), n,
                            CONFS[CHIP][2], CONFS[CHIP][3], ro_check, int(ro_check > 1), 1, 7)
            reader.reset_asic(False, True)
            freq = reader.measure_ro_out(26, 1)[0] # type: ignore
            if (freq == 0) | (freq is None):
                print(f'RO: {ro_check}, frequency is {freq}')
                breaked = True # pylint: disable=invalid-name
                break
            assert isinstance(freq, float)
            ro_pers[ro_check] = 1 / freq * 1e6
            if VERBOSE:
                print(f'RO: {ro_check}, per = {ro_pers[ro_check]} ps')
        if breaked:
            continue
        reader.set_conf(1, 0, CONFS[CHIP][0], CONFS[CHIP][1], 0, 0, n, CONFS[CHIP][2],
                        CONFS[CHIP][3], 0, 0, 0, 0)
        cnts = [0] * NB_SAMPLES
        breaked = False # pylint: disable=invalid-name
        for sample_window in range(int(NB_SAMPLES / 1024)):
            reader.reset_asic(False, True)
            reader.clear_uart_buffers()
            reader.reset_buffers()
            reader.drive_ext_start(2048, 13)
            time.sleep(0.5)
            if reader.get_address()[1] != 1024:
                print(f'Only read out {reader.get_address()[1]} bits!')
                breaked = True # pylint: disable=invalid-name
                break
            cnts[sample_window * 1024:(sample_window + 1) * 1024] = reader.read_buffers(1024) # type: ignore # pylint: disable=line-too-long
        if breaked:
            continue
        if VERBOSE:
            plt.plot(cnts, 'o')
            plt.show()
            print(f'Var: {np.var(cnts)}')
            print('Expected mean: '
                  f'{(ro_pers[0] * 2**n - ro_pers[1] * 2**n + 2 * ro_pers[2]) / ro_pers[3]}')
            print(f'Mean: {np.mean(cnts)}')
        with open(file_name, 'a', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow([*CONFS[CHIP], *ro_pers, 2**n, np.mean(cnts), np.var(cnts)])
        ni += 1
