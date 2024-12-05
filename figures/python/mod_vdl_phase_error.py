"""Generate histogram of repeated simulations illustrating the
absolute phase error figure."""
import argparse
import sys
from os import getcwd
from typing import List, Tuple
import numpy as np
import matplotlib.pyplot as plt
sys.path.append(getcwd())
from lib import graph_maker as g_m # pylint: disable=wrong-import-position
from lib import store_data as s_d # pylint: disable=wrong-import-position
from math_model import math_model as m_m # pylint: disable=wrong-import-position

MOD_JIT_STR = 30e-15
MOD_MU_DC_0 = 2.513e9
MOD_MU_DC_1 = 2.7643e9
MOD_SIGMA_DC_0 = np.sqrt(MOD_JIT_STR) * MOD_MU_DC_0
MOD_SIGMA_DC_1 = np.sqrt(MOD_JIT_STR) * MOD_MU_DC_1
MOD_MU_VDL_0 = 34.558e9
MOD_MU_VDL_1 = 34.805e9
MOD_SIGMA_VDL_0 = np.sqrt(MOD_JIT_STR) * MOD_MU_VDL_0
MOD_SIGMA_VDL_1 = np.sqrt(MOD_JIT_STR) * MOD_MU_VDL_1
MOD_N = 1
MOD_NUM = 1000
MOD_TD_NUM = 100
MOD_TIME_STEP = 2 * np.pi / (max(MOD_MU_VDL_0, MOD_MU_VDL_1)) / 200
HIS_MM: Tuple[float, float] = (0.0, 0.4 * np.pi)
HIS_BINS = 20
HIS_Y_MM: Tuple[float, float] = (0.0, 0.15)

bin_width = (HIS_MM[1] - HIS_MM[0]) / HIS_BINS

parser = argparse.ArgumentParser()
parser.add_argument('-v', help='Print process', action='store_true')
parser.add_argument('-d', help='Collect data', action='store_true')
parser.add_argument('-q', help='Quit after data collect', action='store_true')
args = parser.parse_args()

bin_centers: List[float] = []
rel_corrects: List[float] = []
rel_not_corrects: List[float] = []

store_data = s_d.StoreData(name='mod_vdl_phase_error')

if args.d:
    model_data = m_m.ModelData(MOD_MU_DC_0, MOD_MU_DC_1,
                               MOD_SIGMA_DC_0, MOD_SIGMA_DC_1,
                               MOD_MU_VDL_0, MOD_MU_VDL_1,
                               MOD_SIGMA_VDL_0, MOD_SIGMA_VDL_1,
                               MOD_N)
    approx = m_m.Approx()
    model = m_m.Model(model_data, approx, '')
    td_x_mean = MOD_N * (2 * np.pi / MOD_MU_DC_0 - 2 * np.pi / MOD_MU_DC_1)
    td_x_var: float = MOD_N * np.pi * 2 * MOD_SIGMA_DC_0**2 / MOD_MU_DC_0**3 \
        + MOD_N * np.pi * 2 * MOD_SIGMA_DC_1**2 / MOD_MU_DC_1**3
    td_x_min: float = td_x_mean - 10 * np.sqrt(td_x_var)
    td_x_max: float = td_x_mean + 10 * np.sqrt(td_x_var)
    td_x = [td_x_min + (td_x_max - td_x_min) / MOD_TD_NUM * i for i in range(MOD_TD_NUM)]
    td_y: List[float] = [model.f_cdf_td(x) for x in td_x] # type: ignore

    phi_1s = [0.0] * MOD_NUM
    phi_1s_d = [0.0] * MOD_NUM
    td_s = [0.0] * MOD_NUM
    phi_10s = [0.0] * MOD_NUM
    errs = [0.0] * MOD_NUM
    corrects = [0] * MOD_NUM
    for i in range(MOD_NUM):
        td = 0.0 # pylint: disable=invalid-name
        r = np.random.uniform(0, 1)
        for j in range(MOD_TD_NUM - 1):
            if (td_y[j] <= r) & (td_y[j+1] > r):
                frac = (r - td_y[j]) / (td_y[j+1] - td_y[j])
                td = td_x[j] + frac * (td_x[j+1] - td_x[j])
                break
        phi_0 = 0.0 # pylint: disable=invalid-name
        phi_1 = 0.0 # pylint: disable=invalid-name
        time = 0.0 # pylint: disable=invalid-name
        td_s[i] = td
        if td > 0: #phi1 first
            while time <= td:
                phi_1 += MOD_MU_VDL_1 * MOD_TIME_STEP \
                    + MOD_SIGMA_VDL_1 * np.sqrt(MOD_TIME_STEP) * np.random.normal(0, 1)
                time += MOD_TIME_STEP
        else: #phi0 first
            while time <= -td:
                phi_0 += MOD_MU_VDL_0 * MOD_TIME_STEP \
                    + MOD_SIGMA_VDL_0 * np.sqrt(MOD_TIME_STEP) * np.random.normal(0, 1)
                time += MOD_TIME_STEP
        phi_10s[i] = phi_1
        time = 0.0 # pylint: disable=invalid-name
        init_phase_diff = phi_0 - phi_1
        phase_low = np.floor(init_phase_diff / np.pi) * np.pi
        phase_high = phase_low + np.pi
        while (phase_low < phi_0 - phi_1) & (phase_high > phi_0 - phi_1):
            phi_1 += MOD_MU_VDL_1 * MOD_TIME_STEP \
                + MOD_SIGMA_VDL_1 * np.sqrt(MOD_TIME_STEP) * np.random.normal(0, 1)
            phi_0 += MOD_MU_VDL_0 * MOD_TIME_STEP \
                + MOD_SIGMA_VDL_0 * np.sqrt(MOD_TIME_STEP) * np.random.normal(0, 1)
            time += MOD_TIME_STEP
        phi_1s[i] = np.ceil(phi_1 / 2 / np.pi)
        phi_1s_d[i] = np.ceil((MOD_MU_VDL_1 * (time + max(td, 0))) / (2 * np.pi))
        errs[i] = phi_1 - MOD_MU_VDL_1 * (time + max(td, 0))
        if phi_1s[i] == phi_1s_d[i]:
            corrects[i] = 1
    err = 0.0 # pylint: disable=invalid-name
    for p_1, p_1_d in zip(phi_1s, phi_1s_d):
        err += abs(p_1 - p_1_d) / abs(p_1)
    err /= len(phi_1s)
    if args.v:
        print(f'Relative error: {err}')
    bounds = [HIS_MM[0] + bin_width * i for i in range(HIS_BINS + 1)]
    for i in range(HIS_BINS):
        low = bounds[i]
        high = bounds[i+1]
        num = 0.0 # pylint: disable=invalid-name
        num_correct = 0.0 # pylint: disable=invalid-name
        for er, cor in zip(errs, corrects):
            if (low <= abs(er)) & (high > abs(er)):
                num += 1
                num_correct += cor
        num /= len(errs)
        num_correct /= len(errs)
        x_mid = low + bin_width / 2
        bin_centers.append(x_mid)
        rel_corrects.append(num_correct)
        rel_not_corrects.append(num - num_correct)
    data_to_write = [
        bin_centers,
        rel_corrects,
        rel_not_corrects
    ]
    store_data.write_data(data_to_write, over_write=True)
    if args.q:
        sys.exit()
else:
    if not store_data.file_exist:
        if args.v:
            print(f'File: {store_data.file_path} does not exist!')
        sys.exit()
    data = store_data.read_data()
    if data is None:
        if args.v:
            print(f'Error in data: {store_data.file_path}!')
            sys.exit()
    assert data is not None
    bin_centers, rel_corrects, rel_not_corrects = data

if args.v:
    plt.bar(x=bin_centers, height=rel_corrects, # type: ignore
            width=0.8 * bin_width)
    plt.bar(x=bin_centers, # type: ignore
            height=rel_not_corrects,
            bottom=rel_corrects,
            width=0.8 * bin_width)
    plt.show() # type: ignore

graph_maker = g_m.GraphMaker('mod_vdl_phase_error.svg',
                             figure_size=(1, 1), folder_name='figures')

graph_maker.create_grid(marg_left=0.12)

# Create axes:
ax = graph_maker.create_ax(title='Corrected phase error', # pylint: disable=invalid-name
                           x_label='Phase error',
                           x_unit='rad',
                           y_label='Relative occurrence',
                           y_unit=r'\%',
                           x_scale='fix',
                           y_grid=True,
                           show_legend=True,
                           x_lim=HIS_MM,
                           y_lim=(HIS_Y_MM[0] * 100, HIS_Y_MM[1] * 100),
                           fixed_labels_x=['0', '0.1π', '0.2π', '0.3π'],
                           fixed_locs_x=[0, 0.1 * np.pi, 0.2 * np.pi, 0.3 * np.pi])

# Plot data:
graph_maker.bar_(ax=ax, xs=[b for b, r in zip(bin_centers, rel_not_corrects)if r != 0],
                 ys=[r * 100 - 1.2 * (HIS_Y_MM[1] - HIS_Y_MM[0])
                     for r in rel_not_corrects if r != 0],
                 bottom=[r * 100 + 1.2 * (HIS_Y_MM[1] - HIS_Y_MM[0])
                         for r, rn in zip(rel_corrects, rel_not_corrects) if rn != 0],
                 width=0.8 * bin_width,
                 label='Phase error not corrected',
                 colors=1, alpha=0.5)
graph_maker.bar_(ax=ax, xs=bin_centers,
                 ys=[r * 100 for r in rel_corrects],
                 width=0.8 * bin_width,
                 label='Phase error corrected',
                 colors=0, alpha=0.5)

# Generate SVG:
graph_maker.write_svg()
