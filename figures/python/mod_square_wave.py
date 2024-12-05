"""Generate RO waveform and corresponding phase verusus time figure.
Note! The SVG has to be adjusted to add the X's via Inkscape."""
import argparse
import sys
from os import getcwd
from typing import List, Tuple, cast
import numpy as np
import matplotlib.pyplot as plt
sys.path.append(getcwd())
from lib import graph_maker as g_m # pylint: disable=wrong-import-position
from lib import store_data as s_d # pylint: disable=wrong-import-position

MU: float = 2.0
SIGMA: float= 0.25
PHI_0: float = 0
TIME_STEP: float = 1e-2
TIME_MM: Tuple[float, float] = (0.0, 10.0)
PHI_MM: Tuple[float, float] = (-1.0, 20.0)
SQU_AMP: float = 3.5 * np.pi

nb_points = int((max(TIME_MM) - min(TIME_MM)) / TIME_STEP + 1)

parser = argparse.ArgumentParser()
parser.add_argument('-v', help='Print process', action='store_true')
parser.add_argument('-d', help='Collect data', action='store_true')
parser.add_argument('-q', help='Quit after data collect', action='store_true')
args = parser.parse_args()

mu: float = 0
sigma: float = 0
ts: List[float] = []
phases: List[float] = []
waves: List[float] = []

def e(phi: float) -> float:
    """Waveform function."""
    if phi % (2 * np.pi) < np.pi:
        return SQU_AMP
    return 0

store_data = s_d.StoreData(name='mod_square_wave')

if args.d:
    mu = MU # pylint: disable=invalid-name
    sigma = SIGMA # pylint: disable=invalid-name
    time = TIME_MM[0] # pylint: disable=invalid-name
    ts = [time]
    phases = [PHI_0]
    waves = [e(phases[-1])]
    for _ in range(1, nb_points):
        time += TIME_STEP
        ts.append(time)
        new_p = cast(float, phases[-1] + mu * TIME_STEP \
           + sigma * np.random.normal(0, np.sqrt(TIME_STEP)))
        phases.append(new_p)
        waves.append(e(new_p))

    data_to_write = [[mu], [sigma], ts, phases, waves]
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
    mu = data[0][0]
    sigma = data[1][0]
    ts = data[2]
    phases = data[3]
    waves = data[4]

if args.v:
    plt.plot(ts, phases) # type: ignore
    plt.plot(ts, waves) # type: ignore
    plt.show() # type: ignore

graph_maker = g_m.GraphMaker('mod_square_wave.svg',
                             figure_size=(1, 1), folder_name='figures')
graph_maker.create_grid()

# Create axes:
ax = graph_maker.create_ax(x_slice=0, y_slice=0, # pylint: disable=invalid-name
                           x_scale='lin', y_scale='pi',
                           x_label='Time ($t$)',
                           x_unit='s',
                           y_label=r'Phase ($\Phi$)',
                           y_unit='rad',
                           title=(r'Example realizations of $\Phi(\omega, t)$ '
                                  r'and $(e \circ \Phi)(\omega, t)$'),
                           y_grid=True,
                           show_legend=True,
                           x_lim=TIME_MM,
                           y_lim=PHI_MM,
                           max_nb_y_ticks=8)

# Plot data:
graph_maker.plot(ax=ax, xs=ts, ys=phases,
                 label=(r'$\varphi(t), \; \mu = \SI{'
                        f'{mu:3.1f}'
                        r'}{\per\second}$ $\sigma = \SI{'
                        f'{sigma:4.2f}'
                        r'}{\second\tothe{-0.5}}$'))
graph_maker.plot(ax=ax, xs=ts, ys=waves,
                 label=(r'$w(t) = (e \circ \varphi)(t)$')) # pylint: disable=superfluous-parens

# Generate SVG:
graph_maker.write_svg()
