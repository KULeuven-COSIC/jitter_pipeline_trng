"""Readout a small amount of random samples."""
from typing import List, Tuple, Optional
import sys
import time
import csv
from os import getcwd
from os.path import join, isfile
import numpy as np
sys.path.append(getcwd())
from measurements import read_asic as r_a # pylint: disable=wrong-import-position

CHIP = 1 # Chip
TEMP = 20 # Temperature
SUPPLY = 1.0 # Supply voltage
FILE_INDEX = 2 # File index

NB_SAMPLES = int(2**12) # Number of cnts/bits to extract
BIT_CNT = 1 # Extract bits (0) / counts (1)
VERBOSE = True # Verbose

SAMPLE_WINDOW = 1024 # Sample window 1024
NB_WINDOWS = int(NB_SAMPLES / SAMPLE_WINDOW)

CONF_FILE_NAME = join('measurements', 'm6', f'm6_chip{CHIP:d}_temp{TEMP:d}'
                      f'_sup{SUPPLY:3.1f}_{FILE_INDEX:d}.csv')

def print_(stri: str, end: Optional[str]=None) -> None:
    """Print if verbose."""
    if VERBOSE:
        print(stri, end=end)

confs: List[Tuple[int, int, int, int]] = []
pers: List[Tuple[float, float, float, float]] = []
with open(CONF_FILE_NAME, 'r', encoding='utf-8') as csv_file:
    reader_ = csv.reader(csv_file, delimiter=',')
    next(reader_)
    for row in reader_:
        confs.append((int(row[0]), int(row[1]), int(row[2]), int(row[3])))
        pers.append((float(row[4]), float(row[5]), float(row[6]), float(row[7])))

reader = r_a.AsicReader()
reader.set_period_length(7, True)
reader.set_period_length(5, False)

for i, conf in enumerate(confs):
    per = pers[i]
    print_(f'Start extracting conf {i + 1}/{len(confs)}')
    print_(f'Conf    | {conf[0]:06d} | {conf[1]:06d} | {conf[2]:06d} | {conf[3]:06d}')
    print_(f'Old per | {per[0]:6.2f} | {per[1]:6.2f} | {per[2]:6.2f} | {per[3]:6.2f}')
    new_per: List[Optional[float]] = [None] * 4
    all_good = True # pylint: disable=invalid-name
    for j in range(4):
        reader.set_conf(0, 0, conf[0], conf[1], 0, 1, 0, conf[2], conf[3], j, 1, 1, 7)
        reader.reset_asic(False, True)
        new_p = reader.measure_ro_out(22, 10)
        assert new_p is not None
        if new_p[0] is not None:
            new_per[j] = 1 / np.mean(new_p) * 1e6 # type: ignore
        else:
            print_('RO ' + str(j) + ' could not be read!')
            all_good = False # pylint: disable=invalid-name
            break
    if not all_good:
        print_('Proceed to next conf...')
        continue
    print_(f'New per | {new_per[0]:6.2f} | {new_per[1]:6.2f} | {new_per[2]:6.2f} '
           f'| {new_per[3]:6.2f}')
    bit_file_name = join('measurements', 'm7', f'm7_chip{CHIP:d}_temp{TEMP:d}_'
                         f'sup{SUPPLY:3.1f}_conf{conf[0]:d}-{conf[1]:d}-{conf[2]:d}'
                         f'-{conf[3]:d}.csv')
    if isfile(bit_file_name):
        print_(f'File: {bit_file_name} already exist!')
        continue
    print_(f'Start generating {NB_SAMPLES} samples')
    reader.set_conf(BIT_CNT, 0, conf[0], conf[1], 0, 0, 0, conf[2], conf[3], 0, 0, 0, 7)
    j = 0
    while j < NB_WINDOWS:
        reader.reset_asic(False, True)
        reader.reset_buffers()
        reader.clear_uart_buffers()
        reader.drive_ext_start(SAMPLE_WINDOW * 2, 11)
        time.sleep(0.05)
        nb_samples_read = reader.get_address()[1]
        if nb_samples_read != SAMPLE_WINDOW:
            print_('Could not read out correct amount of samples: '
                    f'{nb_samples_read}/{SAMPLE_WINDOW}')
            reader.set_conf(BIT_CNT, 0, conf[0], conf[1], 0, 0, 0, conf[2], conf[3], 0, 0, 0, 7)
            continue
        cnts = reader.read_buffers(SAMPLE_WINDOW)
        with open(bit_file_name, 'a', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(cnts) # type: ignore
        j += 1
        print_(f'Reading samples {j / NB_WINDOWS * 100:03.0f} %', '\r')
