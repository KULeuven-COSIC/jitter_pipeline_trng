"""Simulation of measurement m5."""
from typing import List
import sys
from os import getcwd
from os.path import join
import csv
import time
import numpy as np
sys.path.append(getcwd())
from math_model import an_simulator as a_s # pylint: disable=wrong-import-position

CHIP = 4

NS = [1, 2, 4, 8]
NOISES = [4.5e-15 * (i + 1) for i in range(19)]

exp_file_name = join('measurements', 'm5', f'm5_chip{CHIP:d}.csv')
sim_file_name = join('math_model', 'simulation_data', 'm5', f'm5_chip{CHIP:d}.csv')

with open (exp_file_name, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader)
    per_dc_0s = []
    per_dc_1s = []
    per_vdl_0s = []
    per_vdl_1s = []
    for row in csv_reader:
        per_dc_0s += [float(row[4]) * 1e-12]
        per_dc_1s += [float(row[5]) * 1e-12]
        per_vdl_0s += [float(row[6]) * 1e-12]
        per_vdl_1s += [float(row[7]) * 1e-12]
pers: List[float] = [np.mean(per_dc_0s), np.mean(per_dc_1s), # type: ignore
                     np.mean(per_vdl_0s), np.mean(per_vdl_1s)] # type: ignore
print(f'pers found: {pers}')


with open(sim_file_name, 'w', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',')
    csv_writer.writerow(['confDC0', 'confDC1', 'confVDL0', 'confVDL1', 'perDC0 [ps]',
                         'perDC1 [ps]', 'perVDL0 [ps]', 'perVDL1 [ps]', 'n', 'cntMean',
                         'cntVar', 'Fnoise [fs]'])

it_times = []
start_time = time.time()

for ni, n in enumerate(NS):
    for noisei, noise in enumerate(NOISES):
        s = a_s.Simulator(noise, *pers, n=n, verbose=False, dc_noise_factor=1) # type: ignore
        expected_mean = int((pers[0] - pers[1] + 2 * pers[2]) / pers[3] + 0.5)
        spread = int(expected_mean / 10 + 0.5)
        xs = list(range(expected_mean - spread, expected_mean + spread))
        pxs = [0.0] * len(xs)
        for i, x_i in enumerate(xs):
            pxs[i] = s.f_pdf_jit_dc_cnt(x_i)
        chksum = sum(pxs)
        while abs(chksum-1) > 1e-2:
            xl = min(xs) - 1
            xh = max(xs) + 1
            if xl >= 0:
                pl = s.f_pdf_jit_dc_cnt(xl)
                pxs = [pl] + pxs
                xs = [xl] + xs
            ph = s.f_pdf_jit_dc_cnt(xh)
            pxs = pxs + [ph]
            xs = xs + [xh]
            chksum = sum(pxs)
        mean = 0.0 # pylint: disable=invalid-name
        var = 0.0 # pylint: disable=invalid-name
        for i, x_i in enumerate(xs):
            mean += x_i * pxs[i]
        for i, x_i in enumerate(xs):
            var += (x_i - mean)**2 * pxs[i]
        with open(sim_file_name, 'a', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow([*[-1] * 4, *[x * 1e12 for x in pers], n, mean, var, noise * 1e15])

        end_time = time.time()
        it_times += [end_time - start_time]
        start_time = end_time
        its_to_do = len(NOISES) - noisei - 1 + (len(NS) - ni - 1) * len(NOISES)
        est_to_do = its_to_do * np.mean(it_times)
        est_hour = int(est_to_do / 3600)
        est_minu = int(est_to_do / 60) % 60
        est_seco = int(est_to_do) % 60
        print(f'ToDo: {est_hour:02d}:{est_minu:02d}:{est_seco:02d}', end='\r')
