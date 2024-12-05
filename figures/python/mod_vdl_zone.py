"""Generate relation between the TDC phases and sampling time instances figure."""
import argparse
import sys
from os import getcwd
from typing import List, Tuple, cast
import numpy as np
import matplotlib.pyplot as plt
sys.path.append(getcwd())
from lib import graph_maker as g_m # pylint: disable=wrong-import-position
from lib import store_data as s_d # pylint: disable=wrong-import-position

MUS: Tuple[float, float] = (6.0, 6.4) # Top: (6.0, 5.6)
SIGMAS: Tuple[float, float] = (0.25, 0.25)
PHI_0S: Tuple[float, float] = (0.0, 0.0)
T_0S: Tuple[float, float] = (0.5, 1.29)
TIME_STEP: float = 1e-2
TIME_MM: Tuple[float, float] = (0.0 * 1e-9, 7.0 * 1e-9)
PHI_MM: Tuple[float, float] = (-1.2 * np.pi, 13 * np.pi)
SQU_AMP: float = 1.0
SQU_MM: Tuple[float, float] = (-0.5 * SQU_AMP, 4.5 * SQU_AMP)

nb_points = int((max(TIME_MM) - min(TIME_MM)) / (TIME_STEP * 1e-9) + 1)

parser = argparse.ArgumentParser()
parser.add_argument('-v', help='Print process', action='store_true')
parser.add_argument('-d', help='Collect data', action='store_true')
parser.add_argument('-q', help='Quit after data collect', action='store_true')
args = parser.parse_args()

ts: List[float] = []
phase_0: List[float] = []
phase_1: List[float] = []
wave_0: List[float] = []
wave_1: List[float] = []
dff: List[float] = []
t_0s: Tuple[float, float] = T_0S

def e(phi: float) -> float:
    """Waveform function."""
    if phi % (2 * np.pi) < np.pi:
        return SQU_AMP
    return 0

store_data = s_d.StoreData(name='mod_vdl_zone')

if args.d:
    time = TIME_MM[0] * 1e9 # pylint: disable=invalid-name
    ts = [time * 1e-9]
    phase_0 = [PHI_0S[0]]
    phase_1 = [PHI_0S[1]]
    wave_0 = [e(phase_0[-1])]
    wave_1 = [e(phase_1[-1])]
    dff = [-1.0]
    for _ in range(1, nb_points):
        time += TIME_STEP
        ts.append(time * 1e-9)
        for mu, sigma, phase, wave, t_0 in zip(MUS, SIGMAS, (phase_0, phase_1),
                                               (wave_0, wave_1), t_0s):
            if time >= t_0:
                phase.append(cast(float, phase[-1] + mu * TIME_STEP \
                                + sigma * np.random.normal(0, np.sqrt(TIME_STEP))))
            else:
                phase.append(phase[-1])
            wave.append(e(phase[-1]))
        closest_pi = int(phase_1[-1] / (2 * np.pi) + 0.5)
        if (phase_1[-1] >= closest_pi * 2 * np.pi) & (phase_1[-2] < closest_pi * 2 * np.pi):
            dff.append(wave_0[-1])
        else:
            dff.append(dff[-1])

    data_to_write: List[List[float]] = [
        ts,
        phase_0, phase_1,
        wave_0, wave_1,
        dff,
        list(t_0s)
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
    ts, phase_0, phase_1, wave_0, wave_1, dff = data[:6]
    t_0s = cast(Tuple[float, float], tuple(data[6]))

if args.v:
    plt.subplot(2, 1, 1) # type: ignore
    plt.plot(ts, phase_0) # type: ignore
    plt.plot(ts, phase_1) # type: ignore
    plt.subplot(2, 1, 2) # type: ignore
    plt.plot(ts, dff) # type: ignore
    plt.plot(ts, [w + 1.5 for w in wave_1]) # type: ignore
    plt.plot(ts, [w + 3 for w in wave_0]) # type: ignore
    plt.show() # type: ignore

graph_maker = g_m.GraphMaker('mod_vdl_zone.svg',
                             figure_size=(1, 1), folder_name='figures')

graph_maker.create_grid(size=(3, 1), y_ratios=[1, 0.05, 1],
                        marg_mid_ver=0, marg_left=0.12)

# Create axes:
ax_ph = graph_maker.create_ax(x_slice=0, y_slice=0, # pylint: disable=invalid-name
                              y_label=r'$\Phi_{TDC_x}$',
                              y_unit='rad',
                              y_scale='pi',
                              x_lim=TIME_MM,
                              y_lim=PHI_MM,
                              x_label_bot=False,
                              x_label_top=True,
                              max_nb_y_ticks=5,
                              y_grid=True,
                              show_legend=True,
                              leg_font_size=0.8)

ax_sw = graph_maker.create_ax(x_slice=0, y_slice=2, # pylint: disable=invalid-name
                              x_label='Time ($t$)',
                              x_unit='s',
                              x_lim=TIME_MM,
                              y_lim=(-0.5, 4 * SQU_AMP + 0.5),
                              y_scale='fix',
                              fixed_locs_y=[0.5 * SQU_AMP, 2 * SQU_AMP, 3.5 * SQU_AMP],
                              fixed_labels_y=['DFF', r'TDC\textsubscript{1}',
                                              r'TDC\textsubscript{0}'])

# Plot data:
graph_maker.plot(ax=ax_ph, xs=ts, ys=phase_0, color=2,
                 label=r'$\Phi_{TDC_0}(\omega, t)$')
graph_maker.plot(ax=ax_ph, xs=ts, ys=phase_1, color=3,
                 label=r'$\Phi_{TDC_1}(\omega, t)$')
i_start = 0 # pylint: disable=invalid-name
while (ts[i_start] < t_0s[0] * 1e-9) | (ts[i_start] < t_0s[1] * 1e-9):
    i_start += 1
nb_pi: int = int(abs(phase_1[i_start] - phase_0[i_start]) / np.pi) + 1
graph_maker.fill_between_y(ax=ax_ph, xs=ts, y0s=[p - nb_pi * np.pi for p in phase_0],
                           y1s=[p - (nb_pi - 1) * np.pi for p in phase_0],
                           where=[(t >= t_0s[0] * 1e-9) & (t >= t_0s[1] * 1e-9) for t in ts],
                           color=2, label=r'$\piup$')
i_eq = i_start # pylint: disable=invalid-name
while int(abs(phase_1[i_eq] - phase_0[i_eq]) / np.pi) + 1 == nb_pi:
    i_eq += 1
graph_maker.plot(ax=ax_ph, xs=[ts[i_eq]], ys=[phase_1[i_eq]], color=1, line_style='none',
                 marker_color=1, marker_edge_color='white', marker='circle')
graph_maker.plot(ax=ax_sw, xs=ts, ys=[s + 3 * SQU_AMP for s in wave_0], color=2)
graph_maker.plot(ax=ax_sw, xs=ts, ys=[s + 1.5 * SQU_AMP for s in wave_1], color=3)
graph_maker.plot(ax=ax_sw, xs=ts, ys=[d if d >= 0 else SQU_AMP for d in dff], color=4)
graph_maker.plot(ax=ax_sw, xs=ts, ys=[0 if d < 0 else None for d in dff], # type: ignore
                 color=4)
graph_maker.fill_between_y(ax=ax_sw, xs=ts, y0s=0, y1s=SQU_AMP,
                           where=[d < 0 for d in dff], color=4)

# Generate SVG:
graph_maker.write_svg()
