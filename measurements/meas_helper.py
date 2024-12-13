"""Measurement helping module."""
from typing import Optional, List, Tuple, Union
import sys
from os import getcwd
from os.path import join, isfile
import csv
from random import randrange
import numpy as np
sys.path.append(getcwd())
from measurements import read_asic as r_a # pylint: disable=wrong-import-position

class MeasHelper:
    """A class containing measurement helping functionality."""

    def __init__(self, chip: int=0, dev: Optional[str]=None):
        self.chip = chip
        self.reader = r_a.AsicReader(dev=dev)
        self.meas_freqs_path = join('measurements', 'm0', f'm0_chip{self.chip}.csv')
        self.delays0p = None
        self.x_dc_0: Optional[List[float]] = None
        self.x_dc_1: Optional[List[float]] = None
        self.x_vdl_0: Optional[List[float]] = None
        self.x_vdl_1: Optional[List[float]] = None
        self.model_degree: Optional[int] = None

    def get_conf(self, ro: int, close_to: Optional[float]=None,
                 min_range: Optional[float]=None, max_range: Optional[float]=None,
                 nb_confs: Optional[int]=None) \
        -> Optional[Union[Tuple[Optional[int], Optional[float]], Tuple[List[int], List[float]]]]:
        """Get an optimal configuration.
        Units always in ps."""
        if not isfile(self.meas_freqs_path):
            print(f'File: {self.meas_freqs_path} does not exist!')
            return None
        per_dc_0s, per_dc_1s, per_vdl_0s, per_vdl_1s = self._get_freqs()
        if ro == 0:
            if close_to is not None:
                return self._find_exact(per_dc_0s, close_to, 0)
            return self._find_range(per_dc_0s, min_range, max_range, nb_confs, 0) # type: ignore
        if ro == 1:
            if close_to is not None:
                return self._find_exact(per_dc_1s, close_to, 1)
            return self._find_range(per_dc_1s, min_range, max_range, nb_confs, 1) # type: ignore
        if ro == 2:
            if close_to is not None:
                return self._find_exact(per_vdl_0s, close_to, 2) # type: ignore
            return self._find_range(per_vdl_0s, min_range, max_range, nb_confs, 2) # type: ignore
        if ro == 3:
            if close_to is not None:
                return self._find_exact(per_vdl_1s, close_to, 3) # type: ignore
            return self._find_range(per_vdl_1s, min_range, max_range, nb_confs, 3) # type: ignore
        return None

    def _find_range(self, pers: List[float], min_range: float, max_range: float,
                    nb_confs: int, ro: int) -> Tuple[List[int], List[float]]:
        pers_c = [x for x in pers]
        zipped = zip(pers_c, range(len(pers)))
        s = sorted(zipped)
        self.reader.set_period_length(7, True)
        self.reader.set_period_length(5, False)
        result_confs: List[int] = []
        result_meass: List[float] = []
        narrow_range = (max_range - min_range) / (max_range + min_range) * 2 < 0.01
        for i, _ in enumerate(pers):
            if ((s[i][0] < min_range) & (not narrow_range)) \
                | ((s[i][0] < 0.95 * min_range) & (narrow_range)):
                continue
            if ((s[i][0] > max_range) & (not narrow_range)) \
                | ((s[i][0] > 1.05 * max_range) & (narrow_range)):
                continue
            if len(result_confs) >= nb_confs:
                break
            conf = s[i][1]
            if ro == 0:
                self.reader.set_conf(0, 0, conf, 0, 0, 1, 0, 0, 0, 0, 0, 1, 7)
            elif ro == 1:
                self.reader.set_conf(0, 0, 0, conf, 0, 1, 0, 0, 0, 1, 0, 1, 7)
            elif ro == 2:
                self.reader.set_conf(0, 0, 0, 0, 0, 0, 0, conf, 0, 2, 1, 1, 7)
            elif ro == 3:
                self.reader.set_conf(0, 0, 0, 0, 0, 0, 0, 0, conf, 3, 1, 1, 7)
            self.reader.reset_asic(False, True)
            freqs = self.reader.measure_ro_out(20, 10)
            if freqs[0] is None: # type: ignore
                continue
            freq = np.mean(freqs) # type: ignore
            assert isinstance(freq, float)
            meas_per: float = 1.0 / freq * 1e6
            if (meas_per > min_range) & (meas_per < max_range):
                result_confs.append(conf)
                result_meass.append(meas_per)
        return (result_confs, result_meass)

    def _find_exact(self, pers: List[float], value: float, ro: int) \
        -> Tuple[Optional[int], Optional[float]]:
        dists = [abs(value - x) for x in pers]
        zipped = zip(dists, range(len(dists)))
        s = sorted(zipped)
        self.reader.set_period_length(7, True)
        self.reader.set_period_length(5, False)
        for i in range(len(dists)):
            conf = s[i][1]
            if ro == 0:
                self.reader.set_conf(0, 0, conf, 0, 0, 1, 0, 0, 0, 0, 0, 1, 7)
            elif ro == 1:
                self.reader.set_conf(0, 0, 0, conf, 0, 1, 0, 0, 0, 1, 0, 1, 7)
            elif ro == 2:
                self.reader.set_conf(0, 0, 0, 0, 0, 0, 0, conf, 0, 2, 1, 1, 7)
            elif ro == 3:
                self.reader.set_conf(0, 0, 0, 0, 0, 0, 0, 0, conf, 3, 1, 1, 7)
            self.reader.reset_asic(False, True)
            freqs = self.reader.measure_ro_out(20, 10)
            assert isinstance(freqs, list)
            for j in freqs:
                if j is None:
                    continue
            freq: float = np.mean(freqs) # type: ignore
            meas_per: float = 1.0 / freq * 1e6
            if abs(meas_per - value) / value < 0.01:
                return (conf, meas_per)
        return (None, None)

    def _get_freqs(self) -> Tuple[List[float], List[float],
                                  List[Optional[float]], List[Optional[float]]]:
        """Get the measured frequency values."""
        with open(self.meas_freqs_path, 'r', encoding='utf-8') as f:
            csv_reader = csv.reader(f, delimiter=',')
            next(csv_reader)
            per_dc_0s: List[float] = []
            per_dc_1s: List[float] = []
            per_vdl_0s: List[Optional[float]] = []
            per_vdl_1s: List[Optional[float]] = []
            for row in csv_reader:
                per_dc_0s.append(float(row[1]) * 1000)
                per_dc_1s.append(float(row[2]) * 1000)
                if (row[3] == 'inf') | (row[4] == 'inf'):
                    per_vdl_0s.append(None)
                    per_vdl_1s.append(None)
                else:
                    per_vdl_0s += [float(row[3])]
                    per_vdl_1s += [float(row[4])]
        return (per_dc_0s, per_dc_1s, per_vdl_0s, per_vdl_1s)

    def read_per(self, ro: int, conf: int, # pylint: disable=dangerous-default-value
                 other_confs: List[int]=[0, 0, 0, 0]) -> Optional[float]:
        """Read out the RO period length."""
        self.reader.set_period_length(7, True)
        if ro == 0:
            self.reader.set_conf(0, 0, conf, other_confs[1], 0, 1, 0, 0, 0, 0, 0, 1, 7)
        elif ro == 1:
            self.reader.set_conf(0, 0, other_confs[0], conf, 0, 1, 0, 0, 0, 1, 0, 1, 7)
        elif ro == 2:
            self.reader.set_conf(0, 0, 0, 0, 0, 0, 0, conf, other_confs[3], 2, 1, 1, 7)
        elif ro == 3:
            self.reader.set_conf(0, 0, 0, 0, 0, 0, 0, other_confs[2], conf, 3, 1, 1, 7)
        self.reader.reset_asic(False, True)
        freqs = self.reader.measure_ro_out(22, 10)
        if freqs[0] is None: # type: ignore
            return None
        freq = np.mean(freqs) # type: ignore
        assert isinstance(freq, float)
        meas_per = 1 / freq * 1e6
        return meas_per

    def _convert_per(self, ro: int, per: float) -> float:
        """Convert the period length."""
        if self.x_dc_0 is None:
            self.build_model()
        assert self.model_degree is not None
        assert self.x_dc_0 is not None
        assert self.x_dc_1 is not None
        assert self.x_vdl_0 is not None
        assert self.x_vdl_1 is not None
        result = 0.0
        for j in range(self.model_degree + 1):
            if ro == 0:
                result += self.x_dc_0[j] * (per**j)
            elif ro == 1:
                result += self.x_dc_1[j] * (per**j)
            elif ro == 2:
                result += self.x_vdl_0[j]*(per**j)
            else:
                result += self.x_vdl_1[j]*(per**j)
        return result

    def build_model(self, nb_model_points: int=10, model_degree: int=2,
                    verbose: bool=False) -> None:
        """Build up the model."""
        per_dc_0s, per_dc_1s, per_vdl_0s, per_vdl_1s = self._get_freqs()
        rand_confs = []
        bui_dc_0s = [0.0] * nb_model_points
        bui_dc_1s = [0.0] * nb_model_points
        bui_vdl_0s = [0.0] * nb_model_points
        bui_vdl_1s = [0.0] * nb_model_points
        i = 0
        if verbose:
            print('Generating {nb_model_points} random confs:')
        while i < nb_model_points:
            conf = randrange(2**16)
            if conf in rand_confs:
                continue
            if per_dc_0s[conf] is None:
                continue
            if per_dc_1s[conf] is None:
                continue
            if per_vdl_0s[conf] is None:
                continue
            if per_vdl_1s[conf] is None:
                continue
            a: List[Optional[float]] = []
            for j in range(4):
                a.append(self.read_per(j, conf))
            good = True
            for j in range(4):
                if a[j] is None:
                    good = False
                    break
            if not good:
                continue
            bui_dc_0s[i] = a[0] # type: ignore
            bui_dc_1s[i] = a[1] # type: ignore
            bui_vdl_0s[i] = a[2] # type: ignore
            bui_vdl_1s[i] = a[3] # type: ignore
            rand_confs += [conf]
            i += 1
        if verbose:
            print('Random confs selected:')
            for i, rc_i in enumerate(rand_confs):
                print(f'Conf {rc_i} roPers: {bui_dc_0s[i]} {bui_dc_1s[i]} {bui_vdl_0s[i]} '
                      f'{bui_vdl_1s[i]}')
        a_dc_0: List[List[float]] = []
        a_dc_1: List[List[float]] = []
        a_vdl_0: List[List[float]] = []
        a_vdl_1: List[List[float]] = []
        b_dc_0 = [0.0] * nb_model_points
        b_dc_1 = [0.0] * nb_model_points
        b_vdl_0 = [0.0] * nb_model_points
        b_vdl_1 = [0.0] * nb_model_points
        for i in range(nb_model_points):
            row_dc_0 = [0.0] * (model_degree + 1)
            row_dc_1 = [0.0] * (model_degree + 1)
            row_vdl_0 = [0.0] * (model_degree + 1)
            row_vdl_1 = [0.0] * (model_degree + 1)
            for j in range(model_degree + 1):
                row_dc_0[j] = per_dc_0s[rand_confs[i]]**(j)
                row_dc_1[j] = per_dc_1s[rand_confs[i]]**(j)
                row_vdl_0[j] = per_vdl_0s[rand_confs[i]]**(j) # type: ignore
                row_vdl_1[j] = per_vdl_1s[rand_confs[i]]**(j) # type: ignore
            a_dc_0.append(row_dc_0)
            a_dc_1.append(row_dc_1)
            a_vdl_0.append(row_vdl_0)
            a_vdl_1.append(row_vdl_1)
            b_dc_0[i] = bui_dc_0s[i]
            b_dc_1[i] = bui_dc_1s[i]
            b_vdl_0[i] = bui_vdl_0s[i]
            b_vdl_1[i] = bui_vdl_1s[i]
        x_dc_0 = np.linalg.lstsq(a_dc_0, b_dc_0, rcond=None)[0]
        x_dc_1 = np.linalg.lstsq(a_dc_1, b_dc_1, rcond=None)[0]
        x_vdl_0 = np.linalg.lstsq(a_vdl_0, b_vdl_0, rcond=None)[0]
        x_vdl_1 = np.linalg.lstsq(a_vdl_1, b_vdl_1, rcond=None)[0]
        if verbose:
            print('Least squares solution for:')
            print(f'DC0: x={x_dc_0}')
            print(f'DC1: x={x_dc_1}')
            print(f'VDL0: x={x_vdl_0}')
            print(f'VDL1: x={x_vdl_1}')
        mse_dc_0 = 0.0
        mse_dc_1 = 0.0
        mse_vdl_0 = 0.0
        mse_vdl_1 = 0.0
        for i in range(nb_model_points):
            y_dc_0 = 0.0
            y_dc_1 = 0.0
            y_vdl_0 = 0.0
            y_vdl_1 = 0.0
            for j in range(model_degree + 1):
                y_dc_0 += x_dc_0[j] * (per_dc_0s[rand_confs[i]]**j)
                y_dc_1 += x_dc_1[j] * (per_dc_1s[rand_confs[i]]**j)
                y_vdl_0 += x_vdl_0[j] * (per_vdl_0s[rand_confs[i]]**j) # type: ignore
                y_vdl_1 += x_vdl_1[j] * (per_vdl_1s[rand_confs[i]]**j) # type: ignore
            mse_dc_0 += (bui_dc_0s[i] - y_dc_0)**2
            mse_dc_1 += (bui_dc_1s[i] - y_dc_1)**2
            mse_vdl_0 += (bui_vdl_0s[i] - y_vdl_0)**2
            mse_vdl_1 += (bui_vdl_1s[i] - y_vdl_1)**2
        mse_dc_0 /= nb_model_points
        mse_dc_1 /= nb_model_points
        mse_vdl_0 /= nb_model_points
        mse_vdl_1 /= nb_model_points
        if verbose:
            print('MSE for:')
            print(f'DC0: {np.sqrt(mse_dc_0)} ps')
            print(f'DC1: {np.sqrt(mse_dc_1)} ps')
            print(f'VDL0: {np.sqrt(mse_vdl_0)} ps')
            print(f'VDL1: {np.sqrt(mse_vdl_1)} ps')
        self.x_dc_0 = x_dc_0 # type: ignore
        self.x_dc_1 = x_dc_1 # type: ignore
        self.x_vdl_0 = x_vdl_0 # type: ignore
        self.x_vdl_1 = x_vdl_1 # type: ignore
        self.model_degree = model_degree

    def get_conf_model(self, ro: int, min_range: float, max_range: float, nb_confs: int=1, # pylint: disable=dangerous-default-value
                       max_check: int=100, verbose: bool=False,
                       other_confs: List[int]=[0, 0, 0, 0], nb_confs_try: int=10) \
        -> Tuple[Union[Optional[List[int]], int], Union[Optional[List[float]], float]]:
        """Get confs from the model."""
        if self.x_dc_0 is None:
            if verbose:
                print('Model not available, building model...')
            self.build_model(verbose=verbose)
        per_dc_0s, per_dc_1s, per_vdl_0s, per_vdl_1s = self._get_freqs()
        pers: List[Optional[float]]
        if ro == 0:
            pers = per_dc_0s # type: ignore
        elif ro == 1:
            pers = per_dc_1s # type: ignore
        elif ro == 2:
            pers = per_vdl_0s
        else:
            pers = per_vdl_1s
        result_confs: List[int] = []
        result_pers: List[float] = []
        mid = (max_range + min_range) / 2
        new_mid = mid
        conf_prev = None
        while len(result_confs) < nb_confs:
            if verbose:
                print(f'Collected {len(result_confs)} confs', end='\r')
            nb_cnt = 0
            pr = None
            prs = None
            same_mids = []
            no_good = True
            while no_good & (nb_cnt < max_check):
                cl_indexes = [0]*nb_confs_try
                cl_dists = [np.inf]*nb_confs_try
                closest_index = 0
                closest_dist = np.inf
                for j, p_j in enumerate(pers):
                    if p_j is None:
                        continue
                    if j in result_confs:
                        continue
                    if j in same_mids:
                        continue
                    new = self._convert_per(ro, pers[j]) # type: ignore
                    if abs(new - new_mid) < closest_dist:
                        closest_index = j
                        closest_dist = abs(new-new_mid)
                    for cli in range(nb_confs_try):
                        if abs(new-new_mid) < cl_dists[cli]:
                            cl_dists = cl_dists[:cli] + [abs(new - new_mid)] + cl_dists[cli:-1]
                            cl_indexes = cl_indexes[:cli] + [j] + cl_indexes[cli:-1]
                            break
                if closest_index == conf_prev:
                    break
                conf_prev = closest_index
                cl_pers: List[Optional[float]] = [0] * nb_confs_try
                for i in range(nb_confs_try-1, -1, -1):
                    cl_pers[i] = self.read_per(ro, cl_indexes[i], other_confs)
                    if cl_pers[i] is None:
                        same_mids += [cl_indexes[i]]
                        del cl_pers[i]
                        del cl_indexes[i]
                        continue
                if len(cl_pers) == 0:
                    continue
                same_mids = []
                cl_diffs = [0.0] * len(cl_indexes)
                for i, _ in enumerate(cl_indexes):
                    cl_diffs[i] = new_mid - cl_pers[i] # type: ignore
                cl_sorted_indexes = [x for _, x in sorted(zip([abs(y) \
                                                               for y in cl_diffs], cl_indexes))]
                cl_sorted_pers = [x for _, x in sorted(zip([abs(y) for y in cl_diffs], cl_pers))]
                in_bounds = [False] * len(cl_sorted_indexes)
                for i, _ in enumerate(cl_sorted_indexes):
                    in_bounds[i] = (min_range < cl_sorted_pers[i]) & (max_range > cl_sorted_pers[i]) # type: ignore # pylint: disable=line-too-long
                    if in_bounds[i]:
                        if no_good:
                            no_good = False
                            pr = []
                            prs = []
                        pr += [cl_sorted_indexes[i]]
                        prs += [cl_sorted_pers[i]]
                new_mid = mid + new_mid - cl_sorted_pers[0] # type: ignore
                nb_cnt += 1
            if pr is not None:
                result_confs += pr
                result_pers += prs # type: ignore
            else:
                break
        if len(result_confs) == 0:
            return (None, None)
        if nb_confs == 1:
            return (result_confs[0], result_pers[0])
        return (result_confs, result_pers)

class BoundCalc:
    """ASIC Optimizer class.
    f_noise comes from jitter estimation, alpha comes from DataReaders/hvsres_reader1,
    beta can be freely chosen, min_vdl_freq can also be chosen
    (should be achievable by hardware).
    """

    def __init__(self, f_noise: float=30e-15, alpha: float=1.94,
                 beta: float=0.1, min_vdl_freq: float=4e9, max_vdl_freq: float=6e9,
                 verbose: bool=False):
        self.f_noise = f_noise
        self.alpha = alpha
        self.beta = beta
        self.max_p_vdl = 1 / min_vdl_freq
        self.min_p_vdl = 1 / max_vdl_freq
        self.verbose = verbose
        self.res_opt: float = ((self.max_p_vdl**2)**(1 / 3) * self.alpha**(2 / 3) \
                               * self.f_noise**(1 / 3)) / (2**(1 / 3))
        self.p_dc_opt: float = ((self.max_p_vdl**2) / (2 * self.alpha \
                                                       * np.sqrt(self.f_noise)))**(2 / 3)

    def get_p_dc1_bounds(self) -> Tuple[float, float]:
        """Get bounds for DC1."""
        max_min = self._get_p_dc_max_min()
        return (max_min[0], max_min[0] + self.beta * max_min[1])

    def get_p_dc_0_bounds(self, p_dc_1: float) -> Tuple[float, float]:
        """Get bounds for DC0."""
        return (p_dc_1 - self.max_p_vdl / 2, p_dc_1)

    def get_p_vdl_1_bounds(self) -> Tuple[float, float]:
        """Get bounds for VDL1."""
        return (self.min_p_vdl, self.max_p_vdl)

    def get_p_vdl_0_bounds(self, p_vdl_1: float, p_dc_1: float) \
        -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """Get bounds for VDL0.
        This will generate two suitable intervals."""
        res_min: float = (self.max_p_vdl**2) / (2 * p_dc_1)
        res_max: float = self.alpha * np.sqrt(self.f_noise * p_dc_1)
        return ((max(self.min_p_vdl, p_vdl_1 - res_max),
                 max(self.min_p_vdl, p_vdl_1 - res_min)),
                (min(self.max_p_vdl, p_vdl_1 + res_min),
                 min(self.max_p_vdl, p_vdl_1 + res_max)))

    def _get_p_dc_max_min(self) -> Tuple[float, float]:
        """DC should fall within [result:result + beta * p_dc_opt]"""
        p_dc_opt: float = ((self.max_p_vdl**2) \
                           / (2 * self.alpha * np.sqrt(self.f_noise)))**(2 / 3)
        self._print('p_dc_opt = {p_dc_opt}')
        res_opt: float = ((self.max_p_vdl**2)**(1 / 3) * self.alpha**(2 / 3) \
                          * self.f_noise**(1 / 3))/(2**(1 / 3))
        self._print('res_opt = {res_opt}')
        p_dc_cur = p_dc_opt
        res_diff = (self._get_bound_2(p_dc_cur) - self._get_bound_1(p_dc_cur)) / res_opt
        while res_diff < self.beta:
            p_dc_cur += 0.001 * p_dc_opt
            res_diff = (self._get_bound_2(p_dc_cur) - self._get_bound_1(p_dc_cur)) / res_opt
        self._print('p_dc found: {p_dc_cur}')
        return (p_dc_cur, p_dc_opt)

    def _get_bound_1(self, p_dc: float) -> float:
        return (self.max_p_vdl**2) / (2*p_dc)

    def _get_bound_2(self, p_dc: float) -> float:
        return self.alpha * np.sqrt(self.f_noise * p_dc)

    def _print(self, stri: str) -> None:
        """Print if verbose."""
        if self.verbose:
            print(stri)
