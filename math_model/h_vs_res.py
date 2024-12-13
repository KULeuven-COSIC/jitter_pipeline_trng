"""Generate entropy versus resolution data."""
import sys
from os import getcwd
from os.path import join
import csv
import numpy as np
sys.path.append(getcwd())
from math_model import an_simulator as a_s # pylint: disable=wrong-import-position

NB_RES = 10
NB_DCS = 7
P_DCS = list(range(500, 25000, 500))

START_RESS = 64 # ps
F_NOISE = 30 # fs
P_VDL_M = 250 # ps

file_name = join('math_model', 'simulation_data', f'h_vs_res_fnoise{int(F_NOISE):d}.csv')

with open(file_name, 'w', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(['F_NOISE [fs]', 'Resolution [ps]', 'PDC0 [ps]', 'PDC1 [ps]',
                     'PVDL0 [ps]', 'PVDL1 [ps]', 'H [bit/bit]'])

for i, p_i in enumerate(P_DCS):
    print(f'P_DCS: {i}')
    ress: float = START_RESS # pylint: disable=invalid-name
    last_p = None # pylint: disable=invalid-name
    last_n = None # pylint: disable=invalid-name
    for j in range(NB_RES):
        print('NB_RES: ' + str(j))
        p_vdl_0 = P_VDL_M - ress / 2 # pylint: disable=invalid-name
        p_vdl_1 = P_VDL_M + ress / 2 # pylint: disable=invalid-name
        p_dc_diff = p_vdl_1 - 0.25 * p_vdl_0 # pylint: disable=invalid-name
        p_dc_0 = p_i + p_dc_diff / 2
        p_dc_1 = p_i - p_dc_diff / 2
        model = a_s.Simulator(F_NOISE * 1e-15, p_dc_0 * 1e-12, p_dc_1 * 1e-12,
                              p_vdl_0 * 1e-12, p_vdl_1 * 1e-12, nb_int=100, verbose=True)
        p1 = model.p_1()
        print(p1)
        h = -p1 * np.log(p1) / np.log(2) - (1 - p1) * np.log(1 - p1) / np.log(2)
        print(h)
        with open (file_name, 'a', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow([F_NOISE, ress, p_dc_0, p_dc_1, p_vdl_0, p_vdl_1, h])
        if h > 0.997:
            if last_n is None:
                ress, last_p = ress * 2, ress
            else:
                ress, last_p = np.sqrt(last_n * ress), ress
        else:
            if last_p is None:
                ress, last_n = ress / 2, ress
            else:
                ress, last_n = np.sqrt(last_p * ress), ress
