"""Generate lower and upper bounds from figure."""
import argparse
import sys
from os import getcwd
from typing import List, Tuple, cast, Callable, Dict, Any
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm # type: ignore
sys.path.append(getcwd())
from lib import graph_maker as g_m # pylint: disable=wrong-import-position
from lib import store_data as s_d # pylint: disable=wrong-import-position

norm_pdf = cast(Callable[[float], float], norm.pdf) # type: ignore

TIME_MMS: List[Tuple[float, float]] = [(1e-2, 10.0), (1e-2, 10.0), (1e-2, 10.0), (1e-2, 10.0)]
Y_MMS: List[Tuple[float, float]] = [(-10.0, 10.0), (-10.0, 10.0), (-10.0, 10.0), (-10.0, 10.0)]
TIME_STEP: float = 1e-2
BOU_MUS: List[float] = [1.0, -1.0, 0.5, -0.5]
BOU_SIGMAS: List[float] = [2.0, 2.0, 0.5, 0.5]
BOU_PHI_0S: List[float] = [np.pi * 3 / 4, np.pi * 3 / 4, np.pi / 2, np.pi / 2]
PDF_MMS: List[Tuple[float, float]] = [(0.0, 2.0), (0.0, 2.0), (0.0, 0.5), (0.0, 0.5)]
PDF_STEP: float = 1e-3
GAU_MAX: float = 0.5
GAU_STEP: float = 1e-2

nb_graphs: int = len(TIME_MMS)
nb_points: List[int] = [int((MM[1] - MM[0]) / TIME_STEP + 1) for MM in TIME_MMS]
nb_gau_steps: List[int] = [int((MM[1] - MM[0]) / GAU_STEP + 1) for MM in Y_MMS]
nb_pdf_steps: List[int] = [int((MM[1] - MM[0]) / PDF_STEP - 1) for MM in TIME_MMS]

parser = argparse.ArgumentParser()
parser.add_argument('-v', help='Print process', action='store_true')
parser.add_argument('-d', help='Collect data', action='store_true')
parser.add_argument('-q', help='Quit after data collect', action='store_true')
args = parser.parse_args()

ts: List[List[float]] = []
ys: List[List[float]] = []
bnd_h: List[List[float]] = []
bnd_l: List[List[float]] = []
gaus: List[List[float]] = []
pdf_ts: List[List[float]] = []
pdfs: List[List[float]] = []
bou_mus: List[float] = []
bou_sigmas: List[float] = []
bou_phi_0s: List[float] = []

store_data = s_d.StoreData(name='mod_tpi_bounds')

if args.d:
    data_to_write: List[List[float]] = []
    for time_mm, y_mm, bou_mu, bou_sigma, bou_phi_0, pdf_mm, \
        nb_point, nb_gau_step, nb_pdf_step \
        in zip(TIME_MMS, Y_MMS, BOU_MUS, BOU_SIGMAS, BOU_PHI_0S, PDF_MMS,
               nb_points, nb_gau_steps, nb_pdf_steps):
        # Bounds:
        time = time_mm[0]
        ts_i: List[float] = []
        bnd_h_i: List[float] = []
        bnd_l_i: List[float] = []
        for _ in range(nb_point):
            ts_i.append(time)
            bnd_h_i.append((np.pi - bou_mu * time - bou_phi_0 % np.pi) \
                           / (bou_sigma * np.sqrt(time)))
            bnd_l_i.append((-bou_mu * time - bou_phi_0 % np.pi) \
                           / (bou_sigma * np.sqrt(time)))
            time += TIME_STEP
        ts.append(ts_i)
        bnd_h.append(bnd_h_i)
        bnd_l.append(bnd_l_i)
        # Gauss:
        y = y_mm[0]
        ys_i: List[float] = []
        gaus_i: List[float] = []
        for _ in range(nb_gau_step):
            ys_i.append(y)
            gaus_i.append(norm.pdf(y)) # type: ignore
            y += GAU_STEP
        ys.append(ys_i)
        gaus.append(gaus_i)
        # PDF:
        time = time_mm[0] + PDF_STEP
        pdf_t_i: List[float] = []
        pdf_i: List[float] = []
        for _ in range(nb_pdf_step):
            tb = (np.pi - bou_mu * time - bou_phi_0 % np.pi) \
                / (bou_sigma * np.sqrt(time))
            bb = (-bou_mu * time - bou_phi_0 % np.pi) \
                / (bou_sigma * np.sqrt(time))
            pdf = - norm_pdf(tb) * ((-bou_mu * time - np.pi + bou_phi_0 % np.pi) \
                                   / (2 * bou_sigma * time * np.sqrt(time))) \
                  + norm_pdf(bb) * ((-bou_mu * time + bou_phi_0 % np.pi) \
                                    / (2 * bou_sigma * time * np.sqrt(time)))
            pdf_t_i.append(time)
            pdf_i.append(pdf)
            time += PDF_STEP
        pdf_ts.append(pdf_t_i)
        pdfs.append(pdf_i)
        data_to_write_i: List[List[float]] = [
            [bou_mu], [bou_sigma], [bou_phi_0],
            ts_i, bnd_h_i, bnd_l_i,
            ys_i, gaus_i,
            pdf_t_i, pdf_i
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
    bou_mu_l = data[::10]
    bou_sigma_l = data[1::10]
    bou_phi_0_l = data[2::10]
    ts, bnd_h, bnd_l, ys, gaus, pdf_ts, pdfs = [data[3 + i::10] for i in range(7)]
    bou_mus = [b[0] for b in bou_mu_l]
    bou_sigmas = [b[0] for b in bou_sigma_l]
    bou_phi_0s = [b[0] for b in bou_phi_0_l]

if args.v:
    for i, (t_i, h_i, l_i, y_i, g_i, pt_i, p_i) \
        in enumerate(zip(ts, bnd_h, bnd_l, ys, gaus, pdf_ts, pdfs)):
        plt.subplot(3, 4, 1 + i) # type: ignore
        plt.plot(y_i, g_i) # type: ignore
        plt.subplot(3, 4, 5 + i) # type: ignore
        plt.plot(pt_i, p_i) # type: ignore
        plt.subplot(3, 4, 9 + i) # type: ignore
        plt.plot(t_i, h_i) # type: ignore
        plt.plot(t_i, l_i) # type: ignore
    plt.show() # type: ignore

graph_maker = g_m.GraphMaker('mod_tpi_bounds.svg',
                             figure_size=(1, 1), folder_name='figures')

graph_maker.create_grid(size=(3, 15),
                        y_ratios=[1, 0.3, 4],
                        x_ratios=[1, 0.05, 5, 0.3, 1, 0.05, 5, 0.3, 1, 0.05, 5, 0.3, 1, 0.05, 5],
                        marg_mid_ver=0, marg_mid_hor=0, marg_left=0, marg_right=0.99,
                        marg_top=1, marg_bot=0.2)

# Create axes:
ax_gs: List[int] = []
ax_ps: List[int] = []
ax_ms: List[int] = []
for i, (time_mm, y_mm, pdf_mm) in enumerate(zip(TIME_MMS, Y_MMS, PDF_MMS)):
    g_pars: Dict[str, Any] = {}
    if not i:
        g_pars['show_legend'] = True
        g_pars['legend_loc'] = 'center'
        g_pars['legend_bbox'] = [12.55, -0.2, 0.0, 0.0]
        g_pars['leg_font_size'] = 0.7
        g_pars['nb_leg_cols'] = 4
    ax_gs_i = graph_maker.create_ax(x_slice=i * 4, # pylint: disable=invalid-name
                                    y_slice=2,
                                    show_x_ticks=False,
                                    show_y_ticks=False,
                                    show_x_labels=False,
                                    show_y_labels=False,
                                    x_lim=(0.0 - 0.2 * GAU_MAX, 1.2 * GAU_MAX),
                                    y_lim=(y_mm[0] - 0.1 * (y_mm[1] - y_mm[0]),
                                           y_mm[1] + 0.1 * (y_mm[1] - y_mm[0])),
                                    hide_x_ticks=True,
                                    hide_y_ticks=True,
                                    x_invert=True,
                                    x_spines='none',
                                    y_spines='none',
                                    **g_pars)
    ax_ps_i = graph_maker.create_ax(x_slice=i * 4 + 2, # pylint: disable=invalid-name
                                    y_slice=0,
                                    show_x_ticks=False,
                                    show_y_ticks=False,
                                    show_x_labels=False,
                                    show_y_labels=False,
                                    x_lim=(time_mm[0] - 0.015 * (time_mm[1] - time_mm[0]),
                                           time_mm[1] + 0.1 * (time_mm[1] - time_mm[0])),
                                    y_lim=(pdf_mm[0] - 0.1 * (pdf_mm[1] - pdf_mm[0]),
                                           pdf_mm[1] + 0.1 * (pdf_mm[1] - pdf_mm[0])),
                                    hide_x_ticks=True,
                                    hide_y_ticks=True,
                                    x_spines='none',
                                    y_spines='none')
    ax_ms_i = graph_maker.create_ax(x_slice=i * 4 + 2, # pylint: disable=invalid-name
                                    y_slice=2,
                                    show_x_ticks=False,
                                    show_x_labels=False,
                                    y_scale='fix',
                                    fixed_locs_y=[0],
                                    fixed_labels_y=[''],
                                    x_lim=(time_mm[0] - 0.015 * (time_mm[1] - time_mm[0]),
                                           time_mm[1] + 0.1 * (time_mm[1] - time_mm[0])),
                                    y_lim=(y_mm[0] - 0.1 * (y_mm[1] - y_mm[0]),
                                           y_mm[1] + 0.1 * (y_mm[1] - y_mm[0])),
                                    hide_x_ticks=True,
                                    hide_y_ticks=True,
                                    show_legend=True,
                                    leg_font_size=0.6,
                                    leg_handle_len=0,
                                    legend_loc='lower center',
                                    leg_column_space=0,
                                    legend_bbox=[0.5, 0.0, 0.0, 0.0],
                                    y_spines='left',
                                    x_spine_center=True,
                                    x_arrow=True,
                                    y_arrow=True)
    ax_gs.append(ax_gs_i)
    ax_ps.append(ax_ps_i)
    ax_ms.append(ax_ms_i)

# Plot data:
for t_i, h_i, l_i, y_i, g_i, pt_i, p_i, \
    mu, sigma, phi_0, \
    ax_g, ax_p, ax_m \
    in zip(ts, bnd_h, bnd_l, ys, gaus, pdf_ts, pdfs,
           bou_mus, bou_sigmas, bou_phi_0s,
           ax_gs, ax_ps, ax_ms):
    graph_maker.fill_between_y(ax=ax_m, xs=t_i, y0s=l_i,
                               y1s=h_i, color=2)
    graph_maker.plot(ax=ax_g, xs=g_i, ys=y_i,
                     color=2)
    graph_maker.plot(ax=ax_p, xs=pt_i, ys=p_i,
                     color=3, zorder=1000)
    graph_maker.plot(ax=ax_m, xs=t_i, ys=h_i,
                     color=0)
    graph_maker.plot(ax=ax_m, xs=t_i, ys=l_i,
                     color=1)
    # Legend entries:
    graph_maker.plot(ax=ax_m, xs=[], ys=[], line_style='none',
                     label=(r'$\mu_{\Delta} = \SI{'
                            f'{mu:3.1f}'
                            r'}{\per\second}$'))
    graph_maker.plot(ax=ax_m, xs=[], ys=[], line_style='none',
                     label=(r'$\sigma_{\Delta} = \SI{'
                            f'{sigma:3.1f}'
                            r'}{\second\tothe{-0.5}}$'))
    graph_maker.plot(ax=ax_m, xs=[], ys=[], line_style='none',
                     label=(r'$\varphi = '
                            f'{(phi_0 / np.pi):4.2f}'
                            r'\piup$'))
    # Main legend:
    graph_maker.plot(ax=ax_g, xs=[], ys=[], visible=False,
                     line_style='solid', color=0,
                     label='Upper bound')
    graph_maker.plot(ax=ax_g, xs=[], ys=[], visible=False,
                     line_style='solid', color=1,
                     label='Lower bound')
    graph_maker.plot(ax=ax_g, xs=[], ys=[], visible=False,
                     line_style='solid', color=2,
                     label=r'$\mathcal{N}(0, 1)$')
    graph_maker.plot(ax=ax_g, xs=[], ys=[], visible=False,
                     line_style='solid', color=3,
                     label=r'$f_{T_{\piup} \mid \Phi_{\Delta}^0}(t \mid \varphi)$')

# Generate SVG:
graph_maker.write_svg()
