"""Read all ro frequencies."""
import sys
from os import getcwd
from os.path import join
import time
import csv
import numpy as np
sys.path.append(getcwd())
from measurements import read_asic as r_a # pylint: disable=wrong-import-position

CHIP = 4
FAULTS = 40
START = 40130
FREQ_SEL = 0

FILE_NAME = join('measurements', 'm0', f'm0_chip{CHIP:d}.csv')
if START == 0:
    with open(FILE_NAME, 'w', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(['conf', 'perDC0 [ns]', 'perDC1 [ns]', 'perVDL0 [ps]',
                             'per VDL1 [ps]', 'CONFFREQ_SEL=' + str(FREQ_SEL)])

reader = r_a.AsicReader()
reader.reset_asic(True, True)
reader.set_period_length(5, True)

NB_CONFS = 2**16
start_time = time.time()
i = START
it_time = time.time()
time_per_it = 1.0 # pylint: disable=invalid-name

while i < NB_CONFS:
    ro_pers = [0.0] * 4
    for ro in range(4):
        same = False # pylint: disable=invalid-name
        number = 0 # pylint: disable=invalid-name
        meas = [0.0] * FAULTS
        freqs = -1.0 # pylint: disable=invalid-name
        while (not same) & (number < FAULTS):
            if ro == 0:
                reader.set_conf(0, 0, i, 0, 0, 1, FREQ_SEL, 0, 0, 0, 0, 1, 7)
            elif ro == 1:
                reader.set_conf(0, 0, 0, i, 0, 1, FREQ_SEL, 0, 0, 1, 0, 1, 7)
            elif ro == 2:
                reader.set_conf(0, 0, 0, 0, 0, 0, 0, i, 0, 2, 1, 1, 7)
            else:
                reader.set_conf(0, 0, 0, 0, 0, 0, 0, 0, i, 3, 1, 1, 7)
            freq = reader.measure_ro_out(20, 10)
            assert freq is not None
            if freq[0] is None:
                freqs = 0.0 # pylint: disable=invalid-name
            else:
                freqs = np.mean(freq) # type: ignore
            meas[number] = freqs
            number += 1
            if (freqs != 0) & (freqs < 1e6):
                for ii in range(number - 1):
                    if abs(meas[ii] - freqs) < freqs / 100:
                        same = True # pylint: disable=invalid-name
                        freqs = (meas[ii] + freqs) / 2
                        break
        if not same:
            print('Conf: {i} {ro}, too many faults!')
            freqs = np.median(meas) # type: ignore
        if ro < 2:
            ro_pers[ro] = 1 / freqs * 1000
        else:
            ro_pers[ro] = 1 / freqs * 1000000
    with open(FILE_NAME, 'a', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow([i, ro_pers[0], ro_pers[1], ro_pers[2], ro_pers[3]])
    it_duration = time.time() - it_time
    it_time = time.time()
    time_per_it = 0.99 * time_per_it + 0.01 * it_duration
    if i % 25 == 0:
        est_to_do = (NB_CONFS - i) * time_per_it
        print(f'Average iteration duration: {time_per_it} sec.')
        print(f'Estimated todo: {int(est_to_do / 3600)}:{int(est_to_do / 60) % 60}'
              f':{int(est_to_do % 60)}')
    i += 1
