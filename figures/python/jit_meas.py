"""Generate jitter measurement results figure."""
import argparse
import sys
import csv
from os import getcwd
from os.path import join
from typing import List, Tuple, Union
import numpy as np
import matplotlib.pyplot as plt
sys.path.append(getcwd())
from lib import graph_maker as g_m # pylint: disable=wrong-import-position
from lib import store_data as s_d # pylint: disable=wrong-import-position

X_MM: Tuple[float, float] = (0.0, 170000e-12)
Y_MM: Tuple[float, float] = (0.0, 0.011)
THEO_JIT: List[float] = [10e3, 20e3, 30e3, 40e3, 50e3]
SELECTED_JIT = 2
CHIPS: List[int] = [0, 1, 2, 3, 4]
EXP_FOLDER = join('measurements', 'm5')
SIM_FOLDER = join('math_model', 'simulation_data', 'm5')

def get_t0_var(r_var_: float, n_: int, t0_per_: float,
               sim_var_: List[float], sim_noise_: List[float]) -> float:
    """Calculate t0_var."""
    if r_var_ > sim_var_[-1]:
        last_delta = sim_var_[-1] - sim_var_[-2]
        noise_delta = sim_noise_[-1] - sim_noise_[-2]
        var_check = sim_var_[-1]
        noise = sim_noise_[-1]
        while var_check < r_var_:
            var_check += last_delta
            noise += noise_delta
        ratio = (r_var_ - (var_check - last_delta)) / last_delta
        noise = ratio * noise + (1 - ratio) * (noise - noise_delta)
    else:
        noise = 0.0
        for i, (sv, sn) in enumerate(zip(sim_var_, sim_noise_)):
            if sv >= r_var_:
                var_delta = sv - sim_var_[i-1]
                ratio = (r_var_ - sim_var_[i-1]) / var_delta
                noise = ratio * sn + (1 - ratio) * sim_noise_[i-1]
                break
    return t0_per_ * n_ * noise / 1000

parser = argparse.ArgumentParser()
parser.add_argument('-v', help='Print process', action='store_true')
parser.add_argument('-d', help='Collect data', action='store_true')
parser.add_argument('-q', help='Quit after data collect', action='store_true')
args = parser.parse_args()

nb_chips = len(CHIPS) # pylint: disable=invalid-name
samples: List[List[List[float]]] = []
acc_times: List[List[float]] = []
chips: List[int] = []

store_data = s_d.StoreData(name='jit_meas')

if args.d:
    chips = CHIPS
    data_to_write: List[List[float]] = []
    for chip in chips:
        exp_file_name = join(EXP_FOLDER, f'm5_chip{chip:d}.csv')
        sim_file_name = join(SIM_FOLDER, f'm5_chip{chip:d}.csv')

        # Read out experimental results:
        per_dc_0_exps: List[float] = []
        per_dc_1_exps: List[float] = []
        per_vdl_0_exps: List[float] = []
        per_vdl_1_exps: List[float] = []
        n_exps: List[int] = []
        cnt_mean_exps: List[float] = []
        cnt_var_exps: List[float] = []
        with open(exp_file_name, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                per_dc_0_exps.append(float(row[4]))
                per_dc_1_exps.append(float(row[5]))
                per_vdl_0_exps.append(float(row[6]))
                per_vdl_1_exps.append(float(row[7]))
                n_exps.append(int(row[8]))
                cnt_mean_exps.append(float(row[9]))
                cnt_var_exps.append(float(row[10]))

        # Read out simulation results:
        per_dc_0_sims: List[float] = []
        per_dc_1_sims: List[float] = []
        per_vdl_0_sims: List[float] = []
        per_vdl_1_sims: List[float] = []
        f_noises: List[float] = []
        n_sims: List[int] = []
        cnt_mean_sims: List[float] = []
        cnt_var_sims: List[float] = []
        with open(sim_file_name, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                per_dc_0_sims.append(float(row[4]))
                per_dc_1_sims.append(float(row[5]))
                per_vdl_0_sims.append(float(row[6]))
                per_vdl_1_sims.append(float(row[7]))
                n_sims.append(int(row[8]))
                cnt_mean_sims.append(float(row[9]))
                cnt_var_sims.append(float(row[10]))
                f_noises.append(float(row[11]))

        # Calculate T0 variance:
        t0_pers: List[float] = []
        t0_vars: List[float] = []
        for r_var, t0_per, n in zip(cnt_var_exps, per_dc_0_exps, n_exps):
            sim_var: List[float] = []
            sim_noise: List[float] = []
            for n_sim, cnt_var_sim, f_noise in zip(n_sims, cnt_var_sims, f_noises):
                if n_sim == n:
                    sim_var.append(cnt_var_sim)
                    sim_noise.append(f_noise)
            t0_vars.append(get_t0_var(r_var, n, t0_per, sim_var, sim_noise))
            t0_pers.append(t0_per * n)

        samples_i: List[List[float]] = []
        accs_i: List[float] = []
        for j in range(4):
            samples_i.append(t0_vars[j::4])
            accs_i.append(np.median(t0_pers[j::4])) # type: ignore
        samples.append(samples_i)
        acc_times.append(accs_i)

        data_to_write_i: List[List[float]] = [
            [chip],
            accs_i,
            *samples_i
        ]
        for d in data_to_write_i:
            data_to_write.append(d)
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
    chip_nbs_l = data[::6]
    acc_times = data[1::6]
    chips = [int(c[0]) for c in chip_nbs_l]
    for ii, _ in enumerate(chips):
        samples.append(data[ii*6 + 2:ii*6 + 6])

if args.v:
    for c, accs, ss in zip(chips, acc_times, samples):
        for a, s in zip(accs, ss):
            plt.plot([a] * len(s), s, 'o') # type: ignore
        plt.show() # type: ignore

graph_maker = g_m.GraphMaker('jit_meas.svg',
                             figure_size=(1, 1), folder_name='figures')

graph_maker.create_grid()

# Create axes:
ax = graph_maker.create_ax(title='Jitter measurement', # pylint: disable=invalid-name
                           x_label=r'DC0 period length',
                           x_unit='s',
                           y_label=r'DC0 period variance',
                           y_unit=r'(ns)\textsuperscript{2}',
                           y_grid=True,
                           show_legend=True,
                           x_lim = X_MM,
                           y_lim=Y_MM,
                           nb_leg_cols=2)

# PLot noise lines:
for jit_index, jit_str in enumerate(THEO_JIT):
    line_style = 'solid' if jit_index == SELECTED_JIT else 'dashed' # pylint: disable=invalid-name
    color: Union[int, str] = 0 if jit_index == SELECTED_JIT else 'grey' # pylint: disable=invalid-name
    alpha = 1 if jit_index == SELECTED_JIT else 0.5 # pylint: disable=invalid-name
    graph_maker.plot(ax=ax, xs=list(X_MM), ys=[x * jit_str for x in X_MM],
                     line_style=line_style, color=color, alpha=alpha)
    graph_maker.text(ax, x=160e-9, y=160e-9 * jit_str, s=f'{int(jit_str * 1e-3)} fs',
                     border_color='white', color=color)

# Plot boxes:
for color, (c, accs, ss) in enumerate(zip(chips, acc_times, samples)):
    for pos, (a, s) in enumerate(zip(accs, ss)):
        graph_maker.violin(ax=ax, data=[s_i * 1e-6 for s_i in s], color=color + 1,
                           alpha=0, position=a * 1e-12,
                           width=5e-9, add_ticks=False, show_box=True)
    graph_maker.fill_between_y(ax=ax, xs=[accs[0] * 1e-12], y0s=ss[0][0] * 1e-6,
                               y1s=ss[0][0] * 1e-6,
                               where=[False], color=color + 1,
                               label=f'Chip {c}', alpha=1)

# Generate SVG:
graph_maker.write_svg()
