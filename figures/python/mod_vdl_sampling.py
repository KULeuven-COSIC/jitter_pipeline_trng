"""Generate relation between TDC phases and sampling time instances figure."""

import argparse
import sys
from os import getcwd
from typing import List, Tuple, cast
import numpy as np
import matplotlib.pyplot as plt
sys.path.append(getcwd())
from lib import graph_maker as g_m # pylint: disable=wrong-import-position
from lib import store_data as s_d # pylint: disable=wrong-import-position

MUS: Tuple[float, float] = (6.0, 5.8)
SIGMAS: Tuple[float, float] = (0.25, 0.25)
PHI_0S: Tuple[float, float] = (0.0, 0.0)
T_0S: Tuple[float, float] = (0.5, 0.75)
TIME_STEP: float = 1e-2
TIME_MM: Tuple[float, float] = (0.0, 10.0e-9)
PHI_MM: Tuple[float, float] = (-0.2 * np.pi, 2.2 * np.pi)
PHI_D_MM: Tuple[float, float] = (-0.1 * np.pi, 1.6 * np.pi)
SQU_MM: Tuple[float, float] = (-0.2, 1.2)
SQU_AMP: float = 1.0

nb_points = int((max(TIME_MM) - min(TIME_MM)) / (TIME_STEP * 1e-9) + 1)

parser = argparse.ArgumentParser()
parser.add_argument('-v', help='Print process', action='store_true')
parser.add_argument('-d', help='Collect data', action='store_true')
parser.add_argument('-q', help='Quit after data collect', action='store_true')
args = parser.parse_args()

mus: Tuple[float, float] = (0.0, 0.0)
sigmas: Tuple[float, float] = (0.0, 0.0)
t_0s: Tuple[float, float] = (0.0, 0.0)
ts: List[float] = []
phi_0s: List[float] = []
phi_1s: List[float] = []
phi_ds: List[float] = []
wave_0s: List[float] = []
wave_1s: List[float] = []
dffs: List[float] = []

def e(phi: float) -> float:
    """Waveform function."""
    if phi % (2 * np.pi) < np.pi:
        return SQU_AMP
    return 0

store_data = s_d.StoreData(name='mod_vdl_sampling')

if args.d:
    mus = MUS
    sigmas = SIGMAS
    t_0s = T_0S
    time = TIME_MM[0] * 1e9 # pylint: disable=invalid-name
    ts = [time * 1e-9]
    phi_0s = [PHI_0S[0]]
    phi_1s = [PHI_0S[1]]
    phi_ds = [phi_0s[-1] - phi_1s[-1]]
    wave_0s = [e(phi_0s[-1])]
    wave_1s = [e(phi_1s[-1])]
    dffs = [-1.0]
    sample_moments: Tuple[List[float], List[float],
                          List[float], List[float]] = ([], [], [], []) #x, BY, TY, DY
    for _ in range(1, nb_points):
        time += TIME_STEP
        ts.append(time * 1e-9)
        for mu, sigma, t_n, phis, waves, phi_0 in zip(mus, sigmas, t_0s, (phi_0s, phi_1s),
                                                      (wave_0s, wave_1s), PHI_0S):
            if time >= t_n:
                phis.append(cast(float, phis[-1] + mu * TIME_STEP \
                                 + sigma * np.random.normal(0, np.sqrt(TIME_STEP))))
                waves.append(e(phis[-1]))
            else:
                phis.append(phi_0)
                waves.append(e(phi_0))
        phi_ds.append(phi_0s[-1] - phi_1s[-1])
        closest_pi = int(phi_1s[-1] / (2 * np.pi) + 0.5)
        if (phi_1s[-1] >= closest_pi * 2 * np.pi) & (phi_1s[-2] < closest_pi * 2 * np.pi):
            dffs.append(wave_0s[-1])
            # Collect sampling moments:
            sample_moments[0].append(time * 1e-9)
            sample_moments[1].append(dffs[-1])
            sample_moments[2].append(wave_0s[-1])
            sample_moments[3].append(phi_ds[-1])
        else:
            dffs.append(dffs[-1])
    data_to_write: List[List[float]] = [
        list(mus), list(sigmas), list(t_0s),
        ts,
        phi_0s, phi_1s, phi_ds,
        wave_0s, wave_1s, dffs,
        *sample_moments
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
    mus = cast(Tuple[float, float], tuple(data[0]))
    sigmas = cast(Tuple[float, float], tuple(data[1]))
    t_0s = cast(Tuple[float, float], tuple(data[2]))
    ts, phi_0s, phi_1s, phi_ds, wave_0s, wave_1s, dffs = data[3:10]
    sample_moments = cast(Tuple[List[float], List[float],
                                List[float], List[float]], tuple((d for d in data[10:])))

if args.v:
    plt.subplot(3, 1, 1) # type: ignore
    plt.plot(ts, phi_ds) # type: ignore
    plt.subplot(3, 1, 2) # type: ignore
    plt.plot(ts, [p % (2 * np.pi) for p in phi_0s]) # type: ignore
    plt.plot(ts, [p % (2 * np.pi) for p in phi_1s]) # type: ignore
    plt.subplot(3, 1, 3) # type: ignore
    plt.plot(ts, [s + 3 for s in wave_0s]) # type: ignore
    plt.plot(ts, [s + 1.5 for s in wave_1s]) # type: ignore
    plt.plot(ts, dffs) # type: ignore
    plt.show() # type: ignore

graph_maker = g_m.GraphMaker('mod_vdl_sampling.svg',
                             figure_size=(1, 1), folder_name='figures')
graph_maker.create_grid(size=(5, 1), y_ratios=[1, 0.05, 1, 0.05, 1],
                        marg_mid_ver=0, marg_left=0.12)

# Create axes:
ax_pd = graph_maker.create_ax(x_slice=0, y_slice=0, # pylint: disable=invalid-name
                              y_label=r'$\Phi_{\Delta}$',
                              y_unit='rad',
                              y_scale='pi',
                              x_lim=TIME_MM,
                              y_lim=PHI_D_MM,
                              x_label_bot=False,
                              x_label_top=True,
                              max_nb_y_ticks=5,
                              y_grid=True)

ax_ph = graph_maker.create_ax(x_slice=0, y_slice=2, # pylint: disable=invalid-name
                              y_label=r'$\Phi_{TDC_x}$',
                              y_unit='rad',
                              y_scale='pi',
                              x_lim=TIME_MM,
                              y_lim=PHI_MM,
                              x_label_bot=False,
                              y_grid=True,
                              max_nb_y_ticks=4)

ax_sw = graph_maker.create_ax(x_slice=0, y_slice=4, # pylint: disable=invalid-name
                              x_label='Time ($t$)',
                              x_unit='s',
                              x_lim=TIME_MM,
                              y_lim=(-0.5, 4 * SQU_AMP + 0.5),
                              y_scale='fix',
                              fixed_locs_y=[0.5 * SQU_AMP, 2 * SQU_AMP, 3.5 * SQU_AMP],
                              fixed_labels_y=['DFF', r'TDC\textsubscript{1}',
                                              r'TDC\textsubscript{0}'])

# Plot data:
p_ds = [p if (t >= t_0s[0] * 1e-9) & (t >= t_0s[1] * 1e-9) else None for t, p in zip(ts, phi_ds)]
graph_maker.plot(ax=ax_pd, xs=ts, ys=p_ds, color=1) # type: ignore

graph_maker.plot(ax=ax_ph, xs=ts, ys=[p % (2 * np.pi) for p in phi_0s], color=2)
graph_maker.plot(ax=ax_ph, xs=ts, ys=[p % (2 * np.pi) for p in phi_1s], color=3)

graph_maker.plot(ax=ax_sw, xs=ts, ys=[s + 3 * SQU_AMP for s in wave_0s], color=2)
graph_maker.plot(ax=ax_sw, xs=ts, ys=[s + 1.5 * SQU_AMP for s in wave_1s], color=3)
graph_maker.plot(ax=ax_sw, xs=ts, ys=[d if d >= 0 else 0 for d in dffs], color=4)
graph_maker.plot(ax=ax_sw, xs=ts, ys=[SQU_AMP if d < 0 else None for d in dffs], # type: ignore
                 color=4)
graph_maker.fill_between_y(ax=ax_sw, xs=ts, y0s=0, y1s=SQU_AMP,
                           where=[d < 0 for d in dffs], color=4)

# Plot samples:
for t_i, dff_i, w1_i, pd_i in zip(*sample_moments):
    graph_maker.plot(ax=ax_sw, xs=[t_i, t_i], ys=[dff_i, w1_i + 3 * SQU_AMP],
                     line_style='dotted', color=0)
    graph_maker.plot(ax=ax_pd, xs=[t_i], ys=[pd_i], line_style='none',
                     color=0, marker='circle', marker_color=0, marker_edge_color='white')
    graph_maker.plot(ax=ax_sw, xs=[t_i], ys=[w1_i + 3 * SQU_AMP], line_style='none',
                     color=0, marker='circle', marker_color=0, marker_edge_color='white')
    graph_maker.plot(ax=ax_sw, xs=[t_i], ys=[dff_i], line_style='none',
                     color=0, marker='circle', marker_color=0, marker_edge_color='white')

# Generate SVG:
graph_maker.write_svg()
