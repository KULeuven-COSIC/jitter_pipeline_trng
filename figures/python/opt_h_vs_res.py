"""Generate minimal alpha required figure."""
import argparse
import sys
import csv
from os import getcwd
from typing import List, Tuple, Optional
import numpy as np
import matplotlib.pyplot as plt
sys.path.append(getcwd())
from lib import graph_maker as g_m # pylint: disable=wrong-import-position
from lib import store_data as s_d # pylint: disable=wrong-import-position

DC_MM: Tuple[float, float] = (0.0, 25e-9)
A_MM = (0.0, 3.5)
CHOSEN_ALPHA = 1.94
F_NOISE = 30.0
H_TARGET = 0.997

file_name = ('/home/adriaan/Desktop/ASIC2021_0_backup_201123/Python/Simulation/'
             f'SimData/mx_Cx_hvsres_{int(F_NOISE)}.csv')

parser = argparse.ArgumentParser()
parser.add_argument('-v', help='Print process', action='store_true')
parser.add_argument('-d', help='Collect data', action='store_true')
parser.add_argument('-q', help='Quit after data collect', action='store_true')
args = parser.parse_args()

xs: List[float] = []
ys: List[float] = []

store_data = s_d.StoreData(name='opt_h_vs_res')

if args.d:
    resolutions: List[float] = []
    p_dc_0s: List[float] = []
    p_dc_1s: List[float] = []
    p_vdl_0s: List[float] = []
    p_vdl_1s: List[float] = []
    h_s: List[float] = []
    with open (file_name, 'r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        next(reader)
        for row in reader:
            resolutions.append(float(row[1]))
            p_dc_0s.append(float(row[2]))
            p_dc_1s.append(float(row[3]))
            p_vdl_0s.append(float(row[4]))
            p_vdl_1s.append(float(row[5]))
            h_s.append(float(row[6]))
    nb_accs = int(len(h_s) / 10) # pylint: disable=invalid-name
    opt_res: List[float] = [0.0] * nb_accs
    dcs: List[float] = [0.0] * nb_accs
    normals: List[float] = [0.0] * nb_accs
    for i in range(nb_accs):
        h_part = h_s[i * 10:(i + 1) * 10]
        res_part = resolutions[i * 10:(i + 1) * 10]
        pdc = max(p_dc_0s[i * 10], p_dc_1s[i * 10])
        close_n: Optional[Tuple[float, float]] = None
        close_p: Optional[Tuple[float, float]] = None
        for j in range(10):
            if h_part[j] < H_TARGET:
                if close_n is None:
                    close_n = (res_part[j], h_part[j])
                else:
                    if (H_TARGET - h_part[j]) < (H_TARGET - close_n[1]):
                        close_n = (res_part[j], h_part[j])
            else:
                if close_p is None:
                    close_p = (res_part[j], h_part[j])
                else:
                    if (h_part[j] - H_TARGET) < (close_p[1] - H_TARGET):
                        close_p = (res_part[j], h_part[j])
        assert close_n is not None
        assert close_p is not None
        frac = (H_TARGET - close_n[1]) / (close_p[1] - close_n[1])
        opt_res[i] = (1 - frac) * close_n[0] + frac * close_p[0]
        dcs[i] = pdc
        normals[i] = opt_res[i] / np.sqrt(F_NOISE * 1e-3 * pdc)
    xs = [d * 1e-12 for d in dcs]
    ys = normals
    data_to_write = [xs, ys]
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
    xs, ys = data

if args.v:
    plt.plot(xs, ys, 'o') # type: ignore
    plt.hlines(CHOSEN_ALPHA, xmin=DC_MM[0], xmax=DC_MM[1]) # type: ignore
    plt.show() # type: ignore

graph_maker = g_m.GraphMaker('opt_h_vs_res.svg',
                             figure_size=(1, 1), folder_name='figures')

graph_maker.create_grid(marg_bot=0.17)

# Create axes:
ax = graph_maker.create_ax(title=r'Minimal $\alpha$ required', # pylint: disable=invalid-name
                           x_label=r'$\max \bigl( \mathbf{E}[T_0^n], \mathbf{E}[T_1^n] \bigr)$',
                           x_unit='s',
                           y_label=r'$\alpha$',
                           y_unit='-',
                           x_grid=True,
                           show_legend=True,
                           x_lim=DC_MM,
                           y_lim=A_MM)

# PLot alpha line:
graph_maker.plot(ax=ax, xs=list(DC_MM), ys=[CHOSEN_ALPHA] * 2,
                 color=1,
                 label=r'Lower bound for $\alpha$')

# Plot dots:
graph_maker.plot(ax=ax, xs=xs, ys=ys, line_style='none',
                 color=0, marker='circle',
                 label=r'$\alpha$ value from model')

# Generate SVG:
graph_maker.write_svg()
