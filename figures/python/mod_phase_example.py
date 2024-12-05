"""Generate example instances of a random phase process figure."""
import argparse
import sys
from os import getcwd
from typing import List, Tuple, cast
import numpy as np
import matplotlib.pyplot as plt
sys.path.append(getcwd())
from lib import graph_maker as g_m # pylint: disable=wrong-import-position
from lib import store_data as s_d # pylint: disable=wrong-import-position

MUS: List[float] = [1, 1, 0.5, 2]
SIGMAS: List[float]	= [1, 2, 1, 1]
PHI0S: List[float] = [0, 0, 0, 0]
TIME_STEP: float = 1e-2
TIME_MM: Tuple[float, float] = (0.0, 10.0)
PHI_MM: Tuple[float, float]	= (-1.0, 20.0)

nb_points = int((max(TIME_MM) - min(TIME_MM)) / TIME_STEP + 1)

parser = argparse.ArgumentParser()
parser.add_argument('-v', help='Print process', action='store_true')
parser.add_argument('-d', help='Collect data', action='store_true')
parser.add_argument('-q', help='Quit after data collect', action='store_true')
args = parser.parse_args()

ts: List[List[float]] = []
ns: List[List[float]] = []
mus: List[float] = []
sigmas: List[float] = []

store_data = s_d.StoreData(name='mod_phase_example')

if args.d:
    mus = MUS
    sigmas = SIGMAS
    for mu, sigma, phi_0 in zip(MUS, SIGMAS, PHI0S):
        time = TIME_MM[0] # pylint: disable=invalid-name
        ts_i = [time]
        ns_i = [phi_0]
        for _ in range(1, nb_points):
            time += TIME_STEP
            ts_i.append(time)
            new_n = cast(float, ns_i[-1] + mu * TIME_STEP \
                         + sigma * np.random.normal(0, np.sqrt(TIME_STEP)))
            ns_i.append(new_n)
        ts.append(ts_i)
        ns.append(ns_i)

    data_to_write: List[List[float]] = []
    for ts_i, ns_i, mu, sigma in zip(ts, ns, MUS, SIGMAS):
        data_to_write += [[mu], [sigma], ts_i, ns_i]
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
    mus_temp = data[::4]
    sigmas_temp = data[1::4]
    ts = data[2::4]
    ns = data[3::4]
    mus = [m[0] for m in mus_temp]
    sigmas = [s[0] for s in sigmas_temp]

if args.v:
    for ts_i, ns_i in zip(ts, ns):
        plt.plot(ts_i, ns_i) # type: ignore
    plt.show() # type: ignore

graph_maker = g_m.GraphMaker('mod_phase_example.svg',
                             figure_size=(1, 1), folder_name='figures')
graph_maker.create_grid()

# Create axes:
ax = graph_maker.create_ax(x_slice=0, y_slice=0, # pylint: disable=invalid-name
                           x_scale='lin', y_scale='pi',
                           x_label='Time ($t$)',
                           x_unit='s',
                           y_label=r'Phase ($\Phi$)',
                           y_unit='rad',
                           title=(r'Example realizations of $\Phi(\omega, t)$'),
                           y_grid=True,
                           show_legend=True,
                           x_lim=TIME_MM,
                           y_lim=PHI_MM,
                           max_nb_y_ticks=8)

# Plot data:
for mu, sigma, ts_i, ns_i in zip(mus, sigmas, ts, ns):
    graph_maker.plot(ax=ax, xs=ts_i, ys=ns_i,
                     label=(r'$\mu = \SI{' f'{mu:3.1f}'
                            r'}{\per\second}$ $\sigma = \SI{'
                            f'{int(sigma):3.1f}' r'}{\second\tothe{-0.5}}$'))

# Generate SVG:
graph_maker.write_svg()
