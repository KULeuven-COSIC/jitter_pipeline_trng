"""Measurement results."""
import argparse
import sys
import csv
from os import getcwd, listdir
from os.path import join, isfile
from typing import List, Tuple, Any, Optional, cast
import matplotlib.pyplot as plt
sys.path.append(getcwd())
from lib import graph_maker as g_m # pylint: disable=wrong-import-position
from lib import store_data as s_d # pylint: disable=wrong-import-position

CHIPS: List[int] = [0, 1, 2, 3, 4]
SUP_CHIP: int = 1
VOLTAGES: List[float] = [0.8, 0.9, 1.0]
F_NOISE: float = 30e-15
MODEL: bool = False
#Core, DC0, DC1, TDC0, TDC1
P_S: List[Tuple[float, float, float]] = [(1.91e-4, 1.33e-5 + 1.43e-5, 6.55e-5 + 6.70e-5),
                                         (2.41e-4, 1.88e-5 + 1.79e-5, 8.26e-5 + 8.47e-5),
                                         (3.27e-4, 2.65e-5 + 2.31e-5, 1.05e-4 + 9.65e-5)]
CHIP_MM: Tuple[float, float] = (-0.5, 4.5)
SUP_MM: Tuple[float, float] = (0.75, 1.05)
H_MM: Tuple[float, float] = (0.9, 0.98)
T_MM: Tuple[float, float] = (200e6, 312.5e6)
P_MM: Tuple[float, float] = (0.0, 0.7e-3)
E_MM: Tuple[float, float] = (1e-12, 2.75e-12)
MIN_H = 0.91

IID_RESULTS_FILE_NAME = join('measurements', 'stat_tests', 'iid_results.txt')
EXP_FOLDER = join('measurements', 'm6')

parser = argparse.ArgumentParser()
parser.add_argument('-v', help='Print process', action='store_true')
parser.add_argument('-d', help='Collect data', action='store_true')
parser.add_argument('-q', help='Quit after data collect', action='store_true')
args = parser.parse_args()

chips: List[int] = []
h_c: List[float] = []
t_c: List[float] = []
sups: List[float] = []
h_s: List[float] = []
t_s: List[float] = []
p_s: List[Tuple[float, float, float]] = []
e_s: List[float] = []

store_data = s_d.StoreData(name='expe_results')

if args.d:
    chips = CHIPS
    sups =VOLTAGES
    p_s = P_S
    h_c = [0] * (max(CHIPS) + 1)
    t_c = [0] * (max(CHIPS) + 1)
    conf_pers = [0] * (max(CHIPS) + 1)
    for chip in CHIPS:
        # Read out NIST IID test results:
        iid_results: List[Tuple[int, List[int], int, float, int, float, bool]] = []
        with open(IID_RESULTS_FILE_NAME, 'r', encoding='utf-8') as iid_file:
            line = iid_file.readline()
            line_nb = 0 # pylint: disable=invalid-name
            while len(line) != 0:
                line_nb += 1
                if line_nb < 5:
                    line = iid_file.readline()
                    continue
                parts = line.split('|')
                chip_ = int(parts[1].split(' ')[1])
                conf = [int(x) for x in parts[2].split(' ')[1:5]]
                temp = int(parts[3].split(' ')[1])
                supply = float(parts[4].split(' ')[1])
                nb_bits = int(parts[5].split(' ')[1])
                h_o = float(parts[6].split(' ')[1])
                h_b = float(parts[7].split(' ')[1])
                chi = parts[8].split(' ')[1] == 'Pass'
                le = parts[9].split(' ')[1] == 'Pass'
                iid = parts[10].split(' ')[1] == 'Pass'
                iid_results.append((chip_, conf, temp, supply, nb_bits,
                                    min(h_o / 8, h_b), (chi & le & iid)))
                line = iid_file.readline()

        # Only look at results of correct chip and high enough entropy
        for i in range(len(iid_results) - 1, -1, -1):
            if iid_results[i][0] != chip:
                del iid_results[i]
                continue
            if iid_results[i][5] < MIN_H:
                del iid_results[i]
                continue
            if not iid_results[i][6]:
                del iid_results[i]
                continue

        # Collect pers for remaining confs:
        m6_conf_files = [f for f in listdir(EXP_FOLDER)
                         if isfile(join(EXP_FOLDER, f)) & (f[1] == '6') & (f[7] == str(chip))]
        m6_conf_files = [f for f in m6_conf_files if f.split('sup')[1].split('_')[0] == '0.9']
        confs: List[Tuple[int, int, int, int]] = []
        pers: List[Tuple[float, float, float, float]] = []
        for f in m6_conf_files:
            conf_file_name = join(EXP_FOLDER, f)
            with open(conf_file_name, 'r', encoding='utf-8') as csv_file:
                reader = csv.reader(csv_file, delimiter=',')
                next(reader)
                for row in reader:
                    confs.append((int(row[0]), int(row[1]), int(row[2]), int(row[3])))
                    pers.append((float(row[4]), float(row[5]), float(row[6]), float(row[7])))
        l = len(iid_results) # pylint: disable=invalid-name
        norm_vol_results: List[List[Any]] = []
        j = 0
        for i in range(l - 1, -1, -1):
            iid_conf = iid_results[i][1]
            found = False # pylint: disable=invalid-name
            for j, con in enumerate(confs):
                if list(con) == iid_conf:
                    found = True # pylint: disable=invalid-name
                    break
            if found:
                norm_vol_results.append(list(iid_results[i]) + [list(pers[j])])
        best_tp = 0.0 # pylint: disable=invalid-name
        best_i: int = 0
        for i, nvr in enumerate(norm_vol_results):
            tp = 1 / max(norm_vol_results[i][7][0], norm_vol_results[i][7][1]) * 1e12
            if tp > best_tp:
                best_tp = tp
                best_i = i
        t_c[chip] = best_tp
        h_c[chip] = norm_vol_results[best_i][5]
        conf_pers[chip] = norm_vol_results[best_i][7]
        if args.v:
            print(chip, norm_vol_results[best_i][1], t_c[chip] / 1e6)

        # Collect different supplys for selected SUPCHIP:
        if chip == SUP_CHIP:
            h_s = [0] * len(VOLTAGES)
            t_s = [0] * len(VOLTAGES)
            vol_i: int = 0
            for voltage in VOLTAGES:
                m6_conf_files = [f for f in listdir(EXP_FOLDER)
                                 if isfile(join(EXP_FOLDER, f)) & (f[1] == '6') \
                                    & (f[7] == str(chip))]
                m6_conf_files = [f for f in m6_conf_files
                                 if f.split('sup')[1].split('_')[0] == str(voltage)]
                confs = []
                pers = []
                for f in m6_conf_files:
                    conf_file_name = join(EXP_FOLDER, f)
                    with open(conf_file_name, 'r', encoding='utf-8') as csv_file:
                        reader = csv.reader(csv_file, delimiter=',')
                        next(reader)
                        for row in reader:
                            confs.append((int(row[0]), int(row[1]), int(row[2]), int(row[3])))
                            pers.append((float(row[4]), float(row[5]),
                                         float(row[6]), float(row[7])))
                l = len(iid_results) # pylint: disable=invalid-name
                vol_results: List[List[Any]] = []
                for i in range(l - 1, -1, -1):
                    iid_conf = iid_results[i][1]
                    found = False # pylint: disable=invalid-name
                    for j, con in enumerate(confs):
                        if list(con) == iid_conf:
                            found = True # pylint: disable=invalid-name
                            break
                    if found:
                        vol_results.append(list(iid_results[i]) \
                                           + [list(pers[j])] + [list(confs[j])])
                best_tp = 0.0 # pylint: disable=invalid-name
                best_i_n: Optional[int] = None
                for i, r in enumerate(vol_results):
                    t_p = 1 / max(r[7][0], r[7][1])*1e12
                    if t_p > best_tp:
                        best_tp = t_p
                        best_i_n = i
                t_s[vol_i] = best_tp
                if best_i_n is not None:
                    h_s[vol_i] = vol_results[best_i_n][5]
                    if args.v:
                        print(voltage, vol_results[best_i_n][8], t_s[vol_i] / 1e6)
                vol_i += 1
    e_s = [sum(p) / t for p, t in zip(p_s, t_s)]
    data_to_write: List[List[float]] = [
        cast(List[float], chips), sups,
        h_c, t_c, h_s, t_s,
        *[[p_i[b_i] for p_i in p_s] for b_i in range(3)],
        e_s
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
    chips_f, sups, h_c, t_c, h_s, t_s = data[:6]
    p_cores, p_dcs, p_tdcs = data[6:9]
    e_s = data[9]
    p_s = [(co, dc, tdc) for co, dc, tdc in zip(p_cores, p_dcs, p_tdcs)]
    chips = [int(c) for c in chips_f]

if args.v:
    plt.subplot(1, 6, 1) # type: ignore
    plt.plot(chips, h_c) # type: ignore
    plt.subplot(1, 6, 2) # type: ignore
    plt.plot(chips, t_c) # type: ignore
    plt.subplot(1, 6, 3) # type: ignore
    plt.plot(sups, h_s) # type: ignore
    plt.subplot(1, 6, 4) # type: ignore
    plt.plot(sups, t_s) # type: ignore
    plt.subplot(1, 6, 5) # type: ignore
    plt.plot(sups, e_s) # type: ignore
    plt.subplot(1, 6, 6) # type: ignore
    plt.bar(sups, [p[0] for p in p_s], width=0.05) # type: ignore
    plt.bar(sups, [p[1] for p in p_s], width=0.05, # type: ignore
            bottom=[p[0] for p in p_s])
    plt.bar(sups, [p[2] for p in p_s], width=0.05, # type: ignore
            bottom=[p[0] + p[1] for p in p_s])
    plt.show() # type: ignore

graph_maker = g_m.GraphMaker('expe_results.svg',
                             figure_size=(1, 1), folder_name='figures')

graph_maker.create_grid(size=(1, 3), marg_mid_hor=1, marg_right=0.91, marg_left=0.09,
                        marg_top=0.8)

# Create axes:
label_size = 0.7 # pylint: disable=invalid-name
ax_c_h = graph_maker.create_ax(x_slice=0, y_slice=0, # pylint: disable=invalid-name
                               x_label='Chip', x_unit='-',
                               y_label='Entropy/bit', y_unit='bit/bit',
                               y_grid=False,
                               x_lim=CHIP_MM,
                               y_lim=H_MM,
                               x_scale='fix',
                               fixed_labels_x=[str(c) for c in chips],
                               fixed_locs_x=cast(List[float], chips),
                               label_font_size=label_size,
                               max_nb_y_ticks=5,
                               y_label_precision=2,
                               y_label_color=0)
ax_c_t = graph_maker.create_twin_ax_x(orig_ax=ax_c_h, # pylint: disable=invalid-name
                                      label='Throughput',
                                      unit='bit/s',
                                      lim=T_MM,
                                      label_font_size=label_size,
                                      max_nb_ticks=5,
                                      label_color=1)
ax_s_h = graph_maker.create_ax(x_slice=1, y_slice=0, # pylint: disable=invalid-name
                               x_label='Supply voltage', x_unit='V',
                               y_label='Entropy/bit', y_unit='bit/bit',
                               y_grid=False,
                               x_lim=SUP_MM,
                               y_lim=H_MM,
                               x_scale='fix',
                               fixed_labels_x=[str(s) for s in sups],
                               fixed_locs_x=sups,
                               label_font_size=label_size,
                               max_nb_y_ticks=5,
                               y_label_precision=2,
                               y_label_color=0,
                               show_legend=True,
                               leg_font_size=0.7,
                               nb_leg_cols=3,
                               legend_bbox=[0.5, 1.15, 0.0, 0.0],
                               legend_loc='center')
ax_s_t = graph_maker.create_twin_ax_x(orig_ax=ax_s_h, # pylint: disable=invalid-name
                                      label='Throughput',
                                      unit='bit/s',
                                      lim=T_MM,
                                      label_font_size=label_size,
                                      max_nb_ticks=5,
                                      label_color=1)
ax_s_p = graph_maker.create_ax(x_slice=2, y_slice=0, # pylint: disable=invalid-name
                               x_label='Supply voltage', x_unit='V',
                               y_label='Power consumption', y_unit='W',
                               y_grid=False,
                               x_lim=SUP_MM,
                               y_lim=P_MM,
                               x_scale='fix',
                               fixed_labels_x=[str(s) for s in sups],
                               fixed_locs_x=sups,
                               label_font_size=label_size,
                               max_nb_y_ticks=5)
ax_s_e = graph_maker.create_twin_ax_x(orig_ax=ax_s_p, # pylint: disable=invalid-name
                                      label='Energy efficiency',
                                      unit='J/bit',
                                      lim=E_MM,
                                      label_font_size=label_size,
                                      max_nb_ticks=5,
                                      label_color=3)
 # Plot data:
graph_maker.plot(ax=ax_c_h, xs=cast(List[float], chips), ys=h_c,
                 line_style='solid', color=0,
                 marker='circle')
graph_maker.plot(ax=ax_c_t, xs=cast(List[float], chips), ys=t_c,
                 line_style='dashed', color=1,
                 marker='cross')
graph_maker.plot(ax=ax_c_h, xs=list(CHIP_MM), ys=[MIN_H] * 2,
                 line_style='dotted', color=2)
graph_maker.text(ax=ax_c_h, x=2, y=MIN_H * 1.003, s=f'{MIN_H}',
                 color=2, border_color='white',
                 font_size=label_size, zorder=1000)

graph_maker.plot(ax=ax_s_h, xs=sups, ys=h_s,
                 line_style='solid', color=0,
                 marker='circle')
graph_maker.plot(ax=ax_s_t, xs=sups, ys=t_s,
                 line_style='dashed', color=1,
                 marker='cross')
graph_maker.plot(ax=ax_s_h, xs=list(SUP_MM), ys=[MIN_H] * 2,
                 line_style='dotted', color=2)
graph_maker.text(ax=ax_s_h, x=0.9, y=MIN_H * 1.003, s=f'{MIN_H}',
                 color=2, border_color='white',
                 font_size=label_size, zorder=1000)

graph_maker.bar_(ax=ax_s_p, xs=sups, ys=[p[0] for p in p_s],
                 width=0.075, colors=4, alpha=0.5)
graph_maker.bar_(ax=ax_s_p, xs=sups,
                 ys=[p[1] - (P_MM[1] - P_MM[0]) * 0.012 for p in p_s],
                 bottom=[p[0] + (P_MM[1] - P_MM[0]) * 0.012 for p in p_s],
                 width=0.075, colors=0, alpha=0.5)
graph_maker.bar_(ax=ax_s_p, xs=sups,
                 ys=[p[2] - (P_MM[1] - P_MM[0]) * 0.012 for p in p_s],
                 bottom=[p[0] + p[1] + (P_MM[1] - P_MM[0]) * 0.012 for p in p_s],
                 width=0.075, colors=1, alpha=0.5)
graph_maker.plot(ax=ax_s_e, xs=sups, ys=e_s,
                 line_style='solid', color=3,
                 marker='star')

# Create legend entries:
graph_maker.plot(ax=ax_s_h, xs=[], ys=[], line_style='solid',
                 color=0, marker='circle', visible=False,
                 label='Entropy density')
graph_maker.fill_between_y(ax=ax_s_h, xs=[], y0s=[], y1s=[], where=[],
                           color=4, alpha=0.5,
                           label='Core power')
graph_maker.plot(ax=ax_s_h, xs=[], ys=[], line_style='dashed',
                 color=1, marker='cross', visible=False,
                 label='Throughput')
graph_maker.fill_between_y(ax=ax_s_h, xs=[], y0s=[], y1s=[], where=[],
                           color=0, alpha=0.5,
                           label='DC power')
graph_maker.plot(ax=ax_s_h, xs=[], ys=[], line_style='solid',
                 color=3, marker='star', visible=False,
                 label='Energy efficiency')
graph_maker.fill_between_y(ax=ax_s_h, xs=[], y0s=[], y1s=[], where=[],
                           color=1, alpha=0.5,
                           label='TDC power')

# Generate SVG:
graph_maker.write_svg()
