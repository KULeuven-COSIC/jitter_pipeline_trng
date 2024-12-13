"""Measured sample correlation obtained from chip 0."""
import argparse
import sys
import csv
from os import getcwd
from os.path import join
from typing import List, Tuple, cast
import numpy as np
import matplotlib.pyplot as plt
sys.path.append(getcwd())
from lib import graph_maker as g_m # pylint: disable=wrong-import-position
from lib import store_data as s_d # pylint: disable=wrong-import-position

CHIP: int = 0
CONF: Tuple[int, int, int, int] = (20809, 2956, 9380, 21184)
TEMP: int = 20
SUP: float = 0.9
COR_LAGS = cast(List[int], list(range(1,1025)))
L_MM: Tuple[float, float] = (min(COR_LAGS)-1, max(COR_LAGS))
C_MM: Tuple[float, float] = (-0.1, 0.1)
RAW_DATA_FOLDER = join('measurements', 'm7')

parser = argparse.ArgumentParser()
parser.add_argument('-v', help='Print process', action='store_true')
parser.add_argument('-d', help='Collect data', action='store_true')
parser.add_argument('-q', help='Quit after data collect', action='store_true')
args = parser.parse_args()

xs: List[int] = []
ys: List[float] = []

store_data = s_d.StoreData(name='expe_count')

if args.d:
    cnt_file_name = join(RAW_DATA_FOLDER,
                         f'm7_chip{CHIP:d}_temp{TEMP:d}_sup{SUP:3.1f}_'
                         f'conf{CONF[0]:d}-{CONF[1]:d}-{CONF[2]:d}-{CONF[3]:d}.csv')
    cnts: List[int] = []
    with open(cnt_file_name, 'r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            for sample in row:
                cnts.append(int(sample))
    cors: List[float] = []
    for lag in COR_LAGS:
        st = 0.0 # pylint: disable=invalid-name
        sn0 = 0.0 # pylint: disable=invalid-name
        sn1 = 0.0 # pylint: disable=invalid-name
        mx: float = np.mean(cnts[:len(cnts) - max(COR_LAGS)]) # type: ignore
        my: float = np.mean(cnts[lag:len(cnts) - max(COR_LAGS) + lag]) # type: ignore
        for j in range(len(cnts) - int(max(COR_LAGS))):
            x = cnts[j]
            y = cnts[j + int(lag)]
            st += (x - mx) * (y - my)
            sn0 += (x - mx)**2
            sn1 += (y - my)**2
        cors.append(st/np.sqrt(sn0*sn1))
    xs = COR_LAGS
    ys = cors
    data_to_write: List[List[float]] = [xs, ys] # type: ignore
    store_data.write_data(data_to_write, over_write=True)
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
    xs, ys = data # type: ignore

if args.v:
    plt.plot(xs, ys, 'o') # type: ignore
    plt.hlines(0, xmin=L_MM[0], xmax=L_MM[1]) # type: ignore
    plt.show() # type: ignore

graph_maker = g_m.GraphMaker('expe_count.svg',
                             figure_size=(1, 1), folder_name='figures')

graph_maker.create_grid(marg_left=0.12)

# Create axes:
ax = graph_maker.create_ax(title=r'Measured sample correlation', # pylint: disable=invalid-name
                           x_label=r'Sample lag',
                           x_unit='sample',
                           y_label=r'Correlation coefficient',
                           y_unit='-',
                           x_grid=True,
                           x_lim=L_MM,
                           y_lim=C_MM)

# Plot dots:
graph_maker.plot(ax=ax, xs=xs, ys=ys, line_style='none', # type: ignore
                 color=0, marker='circle',
                 alpha=0.5,
                 line_width=0.5)

# PLot zero line:
graph_maker.plot(ax=ax, xs=list(L_MM), ys=[0.0] * 2,
                 color=1)

# Generate SVG:
graph_maker.write_svg()
