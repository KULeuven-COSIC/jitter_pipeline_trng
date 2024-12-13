"""Pipelined TRNG stochastic model script."""
from typing import List, Tuple, Optional, Callable, Any
import csv
from concurrent import futures
import numpy as np
from scipy import integrate # type: ignore
from scipy.misc import derivative # type: ignore
from scipy.stats import norm # type: ignore
import matplotlib.pyplot as plt

class ModelData:
    """Container for the model parameters."""

    def __init__(self, mu_dc_0: float, mu_dc_1: float,
                 sigma_dc_0: float, sigma_dc_1: float,
                 mu_vdl_0: float, mu_vdl_1: float,
                 sigma_vdl_0: float, sigma_vdl_1: float,
                 n: int):
        self.mu_dc_0 = mu_dc_0
        self.mu_dc_1 = mu_dc_1
        self.sigma_dc_0 = sigma_dc_0
        self.sigma_dc_1 = sigma_dc_1
        self.mu_vdl_0 = mu_vdl_0
        self.mu_vdl_1 = mu_vdl_1
        self.sigma_vdl_0 = sigma_vdl_0
        self.sigma_vdl_1 = sigma_vdl_1
        self.n = n

    def get_intervals(self) -> List[Tuple[float, float]]: # T_0^n, T_1^n, T_D^n, Phi_D^0, T_pi, R
        """Get the interval."""
        result: List[Tuple[float, float]] = []
        result.append((self.n * 2 * np.pi / self.mu_dc_0 \
                       - 5 * self.sigma_dc_0 * np.sqrt(self.n**3 \
                                                          * 2 * np.pi / self.mu_dc_0**3),
                       self.n * 2 * np.pi / self.mu_dc_0 \
                       + 5 * self.sigma_dc_0 * np.sqrt(self.n**3 \
                                                          * 2 * np.pi / self.mu_dc_0**3)))
        result.append((self.n * 2 * np.pi / self.mu_dc_1 \
                       - 5 * self.sigma_dc_1 * np.sqrt(self.n**3 \
                                                          * 2 * np.pi / self.mu_dc_1**3),
                       self.n * 2 * np.pi / self.mu_dc_1 \
                       + 5 * self.sigma_dc_1 * np.sqrt(self.n**3 \
                                                          * 2 * np.pi / self.mu_dc_1**3)))
        result.append((self.n * 2 * np.pi / self.mu_dc_0 - self.n * 2 * np.pi / self.mu_dc_1 \
                       - 5 * np.sqrt(self.sigma_dc_0**2 * self.n**3 \
                                        * 2 * np.pi / self.mu_dc_0**3 \
                                        + self.sigma_dc_1**2 * self.n**3 \
                                        * 2 * np.pi / self.mu_dc_1**3),
                       self.n * 2 * np.pi / self.mu_dc_0 - self.n * 2 * np.pi / self.mu_dc_1 \
                       + 5 * np.sqrt(self.sigma_dc_0**2 * self.n**3 \
                                        * 2 * np.pi  /self.mu_dc_0**3 \
                                        + self.sigma_dc_1**2 * self.n**3 \
                                        * 2 * np.pi / self.mu_dc_1**3)))
        result.append((- result[2][1] * max(self.mu_vdl_0, self.mu_vdl_1),
                       - result[2][0] * max(self.mu_vdl_0, self.mu_vdl_1)))
        result.append((0, 1 / (self.mu_vdl_0 * abs(2 / self.mu_vdl_0 - 2 / self.mu_vdl_1)) * 1.5))
        result.append((0, int(result[4][1] / (2 * np.pi / self.mu_vdl_1) * 1.1 + 0.5)))
        return result

    def to_csv_lines(self) -> List[List[str]]:
        """Convert to CSV lines."""
        result: List[List[str]] = []
        result.append(['mu_dc_0', 'mu_dc_1', 'sigma_dc_0', 'sigma_dc_1',
                       'mu_vdl_0', 'mu_vdl_1', 'sigma_vdl_0', 'sigma_vdl_1', 'n'])
        result.append([str(self.mu_dc_0), str(self.mu_dc_1),
                       str(self.sigma_dc_0), str(self.sigma_dc_1),
                       str(self.mu_vdl_0), str(self.mu_vdl_1),
                       str(self.sigma_vdl_0), str(self.sigma_vdl_1),
                       str(self.n)])
        return result

class Approx:
    """Approximation class."""

    def __init__(self, size: int=1000, verbose: bool=False):
        self.size = size
        self.verbose = verbose

        self.f_cdf_td_x: Optional[List[float]] = None
        self.f_cdf_td_y: Optional[List[float]] = None
        self.f_cdf_td_interval: Optional[float] = None

        self.f_pdf_td_x: Optional[List[float]] = None
        self.f_pdf_td_y: Optional[List[float]] = None
        self.f_pdf_td_interval: Optional[float] = None
        self.f_pdf_td_bounds: List[Optional[float]] = [None, None]

        self.f_pdf_phid_x: Optional[List[float]] = None
        self.f_pdf_phid_y: Optional[List[float]] = None
        self.f_pdf_phid_interval: Optional[float] = None
        self.f_pdf_phid_bounds: List[Optional[float]] = [None, None]

    def ready_f_cdf_td(self) -> bool:
        """Check if not None."""
        return self.f_cdf_td_x is not None

    def approx_f_cdf_td(self, f: Callable[[float], float], data: ModelData) -> None:
        """Approximate CDF."""
        mean = data.n * 2 * np.pi / data.mu_dc_0 \
               - data.n * 2 * np.pi / data.mu_dc_1
        sigma: float = np.sqrt((data.n * data.sigma_dc_0)**2 + (data.n * data.sigma_dc_1)**2)
        start_t = mean - 5 * sigma
        end_t = mean + 5 * sigma
        if self.verbose:
            print('## F_TD_approx ##')
            print(f'Mean:    {mean}')
            print(f'Sigma:   {sigma}')
            print(f'start_t: {start_t}')
            print(f'end_t:   {end_t}')
        self.f_cdf_td_interval = (end_t - start_t) / self.size
        self.f_cdf_td_x = [0.0] * self.size
        self.f_cdf_td_y = [0.0] * self.size
        for i in range(self.size):
            if self.verbose:
                if int(i / self.size * 1000 + 0.5) % 10 == 0:
                    print(f'{int(i / self.size * 100 + 0.5)}% completed...')
            xi = i / self.size * (end_t - start_t) + start_t
            self.f_cdf_td_x[i] = xi
            self.f_cdf_td_y[i] = f(xi)

    def approx_eval_f_cdf_td(self, t: float) -> float:
        """Approximate evaluation."""
        assert self.f_cdf_td_x is not None
        assert self.f_cdf_td_y is not None
        assert self.f_cdf_td_interval is not None
        if t < self.f_cdf_td_x[0]:
            return 0.0
        if t > self.f_cdf_td_x[-1]:
            return 1.0
        for i in range(self.size - 1):
            if (t >= self.f_cdf_td_x[i]) & (t <= self.f_cdf_td_x[i+1]):
                frac = (t - self.f_cdf_td_x[i]) / self.f_cdf_td_interval
                return self.f_cdf_td_y[i] * (1 - frac) + self.f_cdf_td_y[i+1] * frac
        return -1.0

    def ready_f_pdf_td(self) -> bool:
        """Check if not None."""
        return self.f_pdf_td_x is not None

    def approx_f_pdf_td(self, f, data: ModelData, model) -> None:
        """Approximate PDF."""
        mean = data.n * 2 * np.pi / data.mu_dc_0 - data.n * 2*np.pi / data.mu_dc_1
        sigma: float = np.sqrt(data.sigma_dc_0**2 * data.n**3 * 2 * np.pi / data.mu_dc_0**3 \
                           + data.sigma_dc_1**2 * data.n**3 * 2 * np.pi / data.mu_dc_1**3)
        start_t = mean - 5 * sigma
        end_t = mean + 5 * sigma
        if self.verbose:
            print('## f_TD_approx ##')
            print(f'Mean:    {mean}')
            print(f'Sigma:   {sigma}')
            print(f'start_t: {start_t}')
            print(f'end_t:   {end_t}')
        self.f_pdf_td_interval = (end_t - start_t) / self.size
        self.f_pdf_td_x = [0.0] * self.size
        self.f_pdf_td_y = [0.0] * self.size

        pool = futures.ProcessPoolExecutor(self.size)
        future: List[futures.Future] = []
        for i in range(self.size):
            xi = i / self.size * (end_t - start_t) + start_t
            self.f_pdf_td_x[i] = xi
            future.append(pool.submit(f, model, xi))
        for i in range(self.size):
            futures.wait([future[i]])
            self.f_pdf_td_y[i] = future[i].result()
            if self.verbose:
                if int(i / self.size * 1000 + 0.5) % 10 == 0:
                    print(f'{int(i / self.size * 100 + 0.5)}% completed...')
        self.set_td_bounds()

    def approx_eval_f_pdf_td(self, t: float) -> float:
        """Approximate evaluation."""
        assert self.f_pdf_td_x is not None
        assert self.f_pdf_td_interval is not None
        assert self.f_pdf_td_y is not None
        if t < self.f_pdf_td_x[0]:
            return 0.0
        if t > self.f_pdf_td_x[-1]:
            return 0
        for i in range(self.size - 1):
            if (t >= self.f_pdf_td_x[i]) & (t <= self.f_pdf_td_x[i + 1]):
                frac = (t - self.f_pdf_td_x[i]) / self.f_pdf_td_interval
                return self.f_pdf_td_y[i] * (1 - frac) + self.f_pdf_td_y[i + 1] * frac
        return -1.0

    def set_td_bounds(self) -> List[float]:
        """Set the td bounds."""
        if self.f_pdf_td_x is not None:
            assert self.f_pdf_td_y is not None
            m = max(self.f_pdf_td_y)
            for i, x_i in enumerate(self.f_pdf_td_x):
                if self.f_pdf_td_y[i] > 0.0001 * m:
                    self.f_pdf_td_bounds[0] = x_i
                    break
            for i in range(len(self.f_pdf_td_x)-1, -1, -1):
                if self.f_pdf_td_y[i] > 0.0001 * m:
                    self.f_pdf_td_bounds[1] = self.f_pdf_td_x[i]
                    break
        print(f'f_pdf_td bounds set: {self.f_pdf_td_bounds}')
        return self.f_pdf_td_bounds # type: ignore

    def ready_f_pdf_phid(self) -> bool:
        """Check if not None."""
        return self.f_pdf_phid_x is not None

    def approx_f_pdf_phid(self, f: Callable[[float], float],
                          interval: Tuple[float, float]) -> None:
        """Approximate PDF phid."""
        start_t = interval[0]
        end_t = interval[1]
        if self.verbose:
            print('## Phi_D_approx ##')
            print(f'start_t: {start_t}')
            print(f'end_t:   {end_t}')
        self.f_pdf_phid_interval = (end_t - start_t) / self.size
        self.f_pdf_phid_x = [0.0] * self.size
        self.f_pdf_phid_y = [0.0] * self.size
        for i in range(self.size):
            if self.verbose:
                if int(i / self.size * 1000 + 0.5) % 10 == 0:
                    print(f'{int(i/self.size*100+0.5)}% completed...')
            xi = i / self.size * (end_t - start_t) + start_t
            self.f_pdf_phid_x[i] = xi
            self.f_pdf_phid_y[i] = f(xi)
        self.set_phid_bounds()

    def approx_eval_f_pdf_phid(self, phi: float) -> float:
        """Approximate evaluation for phid PDF."""
        assert self.f_pdf_phid_x is not None
        assert self.f_pdf_phid_y is not None
        assert self.f_pdf_phid_interval is not None
        if phi < self.f_pdf_phid_x[0]:
            return 0.0
        if phi > self.f_pdf_phid_x[-1]:
            return 0.0
        for i in range(self.size - 1):
            if (phi >= self.f_pdf_phid_x[i]) & (phi <= self.f_pdf_phid_x[i + 1]):
                frac = (phi - self.f_pdf_phid_x[i]) / self.f_pdf_phid_interval
                return self.f_pdf_phid_y[i] * (1 - frac) + self.f_pdf_phid_y[i + 1] * frac
        return -1.0

    def set_phid_bounds(self) -> List[float]:
        """Set phid bounds."""
        if self.f_pdf_phid_x is not None:
            assert self.f_pdf_phid_y is not None
            m = max(self.f_pdf_phid_y)
            for i, x_i in enumerate(self.f_pdf_phid_x):
                if self.f_pdf_phid_y[i] > 0.0001 * m:
                    self.f_pdf_phid_bounds[0] = x_i
                    break
            for i in range(len(self.f_pdf_phid_x) - 1, -1, -1):
                if self.f_pdf_phid_y[i] > 0.0001 * m:
                    self.f_pdf_phid_bounds[1] = self.f_pdf_phid_x[i]
                    break
        print(f'f_pdf_phid bounds set: {self.f_pdf_phid_bounds}')
        return self.f_pdf_phid_bounds # type: ignore

class Model:
    """The stochastic model class."""

    def __init__(self, model_data: ModelData, approx: Approx, file_name: str='model.csv'):
        self.model_data = model_data
        self.approx = approx
        self.file_name = file_name

    def f_pdf_ig(self, x: float, mu: float, la: float) -> float:
        """Inverse Gaussian PDF."""
        if x == 0:
            return 0
        return np.sqrt(la / 2 / np.pi / x**3) * np.exp(-la * (x - mu)**2 / (2 * mu**2 * x))

    def inner_p(self, t: float, t1: float, mu: float, la: float) -> float:
        """Integrate."""
        i = integrate.quad(lambda t0: self.f_pdf_ig(t0, mu, la), 0, t + t1)
        return i[0]

    def outer_p(self, t: float, mu1: float, la1: float, mu0: float, la0: float,
                double: bool=False, upper_lim: float=np.inf) -> float:
        """Integrate."""
        if double:
            i = integrate.dblquad(lambda t0, t1: self.f_pdf_ig(t1, mu1, la1) \
                                    * self.f_pdf_ig(t0, mu0, la0),
                                  0, mu1 + upper_lim, lambda _: 0, lambda t1: t+t1)
            return i[0]
        i = integrate.quad(lambda t1: self.f_pdf_ig(t1, mu1, la1) * self.inner_p(t, t1, mu0, la0),
                           0, mu1+upper_lim)
        return i[0]

    def inner_n(self, t: float, t0: float, mu: float, la: float, upper_lim: float=np.inf) -> float:
        """Integrate."""
        i = integrate.quad(lambda t1: self.f_pdf_ig(t1, mu, la), t0 - t, mu + upper_lim)
        return i[0]

    def outer_n(self, t: float, mu1: float, la1: float, mu0: float, la0: float,
                double: bool=False, upper_lim: float=np.inf) -> float:
        """Integrate."""
        if double:
            i = integrate.dblquad(lambda t1, t0: self.f_pdf_ig(t0, mu0, la0) \
                                    * self.f_pdf_ig(t1, mu1, la1),
                                  0, mu0+upper_lim, lambda t0: t0 - t, lambda _: mu1 + upper_lim)
            return i[0]
        i = integrate.quad(lambda t0: self.f_pdf_ig(t0, mu0, la0) \
                            * self.inner_n(t, t0, mu1, la1, upper_lim),
                           0, mu0 + upper_lim)
        return i[0]

    def f_cdf_td(self, t: float, double: bool=False, fast: bool=False) -> float:
        """Get td CDF."""
        if fast:
            if not self.approx.ready_f_cdf_td():
                self.approx.approx_f_cdf_td(lambda t: self.f_cdf_td(t, double, False),
                                            self.model_data)
            return self.approx.approx_eval_f_cdf_td(t)
        mui0 = self.model_data.n * 2 * np.pi / self.model_data.mu_dc_0
        mui1 = self.model_data.n * 2 * np.pi / self.model_data.mu_dc_1
        lai0 = (self.model_data.n * 2 * np.pi / self.model_data.sigma_dc_0)**2
        lai1 = (self.model_data.n * 2 * np.pi / self.model_data.sigma_dc_1)**2
        sigma = np.sqrt(np.pi * self.model_data.n**3 \
                        * max(self.model_data.sigma_dc_0**2 / self.model_data.mu_dc_0**3,
                              self.model_data.sigma_dc_1**2 / self.model_data.mu_dc_1**3))
        if t >= 0:
            return self.outer_p(t, mui1, lai1, mui0, lai0, double, 5 * sigma)
        return self.outer_n(t, mui1, lai1, mui0, lai0, double, 5 * sigma)

    def f_pdf_td(self, t: float, double: bool=False, fast: bool=False) -> float:
        """Get tdc PDF."""
        if fast:
            if not self.approx.ready_f_pdf_td():
                self.approx.approx_f_pdf_td(execute_f_pdf_td_slow, self.model_data, self)
            return self.approx.approx_eval_f_pdf_td(t)
        return derivative(lambda t0: self.f_cdf_td(t0, double, fast), t, 0.0001)

    def f_cdf_phid(self, phi: float, t: float) -> float:
        """Get phid CDF."""
        if t > 0:
            return norm.cdf(phi, -self.model_data.mu_vdl_1 * t,
                            self.model_data.sigma_vdl_1 * np.sqrt(t))
        elif t < 0:
            return norm.cdf(phi, -self.model_data.mu_vdl_0 * t,
                            self.model_data.sigma_vdl_0 * np.sqrt(-t))
        if phi < 0:
            return 0.0
        return 1.0

    def f_pdf_phid(self, phi: float, t: float) -> float:
        """Get phid PDF."""
        if t > 0:
            return norm.pdf(phi, -self.model_data.mu_vdl_1 * t,
                            self.model_data.sigma_vdl_1 * np.sqrt(t))
        elif t < 0:
            return norm.pdf(phi, -self.model_data.mu_vdl_0 * t,
                            self.model_data.sigma_vdl_0 * np.sqrt(-t))
        if phi == 0:
            return np.inf
        return 0.0

    # Without condition to t:
    def f_pdf_phid_nc(self, phi: float, double: bool=False, fast: bool=True) -> float:
        """Get non conditioned phid PDF."""
        if fast:
            if not self.approx.ready_f_pdf_phid():
                interval = self.model_data.get_intervals()[3]
                print(f'f_pdf_phid interval: {interval}')
                self.approx.approx_f_pdf_phid(lambda phi: self.f_pdf_phid_nc(phi, double, False),
                                              interval)
            return self.approx.approx_eval_f_pdf_phid(phi)
        if not self.approx.ready_f_pdf_td():
            self.approx.approx_f_pdf_td(execute_f_pdf_td_slow, self.model_data, self)
        i = self.integrate_single(lambda t: self.f_pdf_phid(phi, t) \
                                    * self.f_pdf_td(t, double, True),
                                  self.approx.f_pdf_td_bounds[0], # type: ignore
                                  self.approx.f_pdf_td_bounds[1], 1000) # type: ignore
        return i

    def f_cdf_t_pi(self, t: float, phi: float) -> float:
        """Get t_pi CDF."""
        mu_d = self.model_data.mu_vdl_0 - self.model_data.mu_vdl_1
        sigma_d = np.sqrt(self.model_data.sigma_vdl_0**2 + self.model_data.sigma_vdl_1**2)
        if t > 0:
            return 1 - norm.cdf((np.pi - mu_d * t - phi % np.pi) / (sigma_d * np.sqrt(t))) \
                + norm.cdf(-(mu_d * t+phi % np.pi) / (sigma_d * np.sqrt(t)))
        return 0.0

    def f_pdf_t_pi(self, t: float, phi: float, analytic: bool=False) -> float:
        """Get t_pi PDF."""
        if analytic:
            if t > 0:
                mu_d = self.model_data.mu_vdl_0 - self.model_data.mu_vdl_1
                sigma_d = np.sqrt(self.model_data.sigma_vdl_0**2 + self.model_data.sigma_vdl_1**2)
                return -norm.pdf((np.pi - mu_d * t - phi % np.pi) / (sigma_d * np.sqrt(t))) \
                    * ((-mu_d * t - np.pi + phi%np.pi) / (2 * sigma_d * t * np.sqrt(t))) \
                    + norm.pdf((-mu_d * t - phi % np.pi) / (sigma_d * np.sqrt(t))) \
                    * ((-mu_d * t + phi % np.pi) / (2 * sigma_d * t * np.sqrt(t)))
            return 0.0
        if t > 0:
            return derivative(lambda ti: self.f_cdf_t_pi(ti, phi), t, 0.0001)
        return 0

    def f_cdf_rc(self, r: int, phi: float, t: float) -> float:
        """Get rc CDF."""
        if t > 0:
            return self.f_cdf_t_pi((2 * np.pi * r + phi) / (self.model_data.mu_vdl_1), phi)
        return self.f_cdf_t_pi((2 * np.pi * r) / (self.model_data.mu_vdl_1), phi)

    def f_pdf_rc(self, r: int, phi: float, t: float) -> float:
        """Get rc PDF."""
        if r > 0:
            return self.f_cdf_rc(r, phi, t) - self.f_cdf_rc(r - 1, phi, t)
        return self.f_cdf_rc(0, phi, t)

    def f_pdf_rj(self, r: int, phi: float, t: float, double: bool=False, fast: bool=False) -> float:
        """Get rj PDF."""
        return self.f_pdf_rc(r, phi, t) * self.f_pdf_phid(phi, t) * self.f_pdf_td(t, double, fast)

    def inner_r(self, r: int, phi: float, fast: bool=False) -> float:
        """Integrate."""
        i = integrate.quad(lambda t: self.f_pdf_rj(r, phi, t, False, fast),
                           -np.inf, np.inf, epsrel=1e-2)
        return i[0]

    def f_pdf_r(self, r: int, double: bool=False, # pylint: disable=dangerous-default-value
                fast: bool=False,
                bounds_phi: List[float]=[-np.inf, np.inf],
                bounds_t: List[float]=[-np.inf, np.inf],
                super_fast: bool=False) -> float:
        """Get r PDF."""
        if super_fast:
            return self.integrate_double(lambda phi, t: self.f_pdf_rj(r, phi, t, True, True),
                                        bounds_phi[0] - 1, bounds_phi[1] + 1,
                                        lambda _: bounds_t[0], lambda _: bounds_t[1], 200, 0)
        if double:
            i = integrate.dblquad(lambda t, phi: self.f_pdf_rj(r, phi, t, True, fast),
                                  bounds_phi[0], bounds_phi[1],
                                  lambda _: bounds_t[0], lambda _: bounds_t[1])
            return i[0]
        i = integrate.quad(lambda phi: self.inner_r(r, phi, fast), -np.inf, np.inf, epsrel=1e-2)
        return i[0]

    def p_b1(self, index: Optional[int]=None) -> float:
        """Get 1 probability."""
        data = self.get_csv_data(index)
        result = 0.0
        check = 0.0
        for i in range(len(data[-1][1])):
            result += (data[-1][0][i] % 2) * data[-1][1][i]
            check += data[-1][1][i]
        if check == 0:
            return 0
        return result / check

    def integrate_double(self, f: Callable[[float, float], float],
                         bound_min_0: float, bound_max_0: float,
                         bound_min_1: Callable[[float], float],
                         bound_max_1: Callable[[float], float],
                         number_squares: int, power: int):
        """Perform a 2D integration."""
        result = 0.0
        interval0 = (bound_max_0 - bound_min_0) / number_squares
        for i0 in range(number_squares):
            x0 = i0 / number_squares * (bound_max_0 - bound_min_0) + bound_min_0
            bounds1 = (bound_min_1(x0), bound_max_1(x0))
            interval1 = (bounds1[1] - bounds1[0]) / number_squares
            for i1 in range(number_squares):
                x1 = i1/number_squares * (bounds1[1] - bounds1[0]) + bounds1[0]
                if power == 0:
                    f00 = f(x0 + interval0/2, x1 + interval1 / 2)
                    result += f00 * interval0 * interval1
                elif power == 1:
                    f00 = f(x0, x1)
                    f10 = f(x0 + interval0, x1)
                    f01 = f(x0, x1 + interval1)
                    a = (f10 - f00) / interval0
                    b = (f01 - f00) / interval1
                    result += f00 * interval0 * interval1 \
                        + a * interval1 * interval0**2 / 2 \
                        + b * interval0 * interval1**2 / 2
        return result

    def integrate_single(self, f: Callable[[float], float],
                         bound_min: float, bound_max: float,
                         number_squares: int) -> float:
        """Perform a 1D integration."""
        result = 0.0
        interval = (bound_max - bound_min) / number_squares
        for i in range(number_squares):
            xi = (i + 0.5) * interval + bound_min
            result += f(xi) * interval
        return result

    def integrate_single_auto(self, f: Callable[[float], float],
                              est_bound_min: float,
                              est_bound_max: float,
                              number_squares: int, max_it: int):
        """Integrate."""
        result = 0.0
        interval = (est_bound_max - est_bound_min) / number_squares
        mid = (est_bound_max + est_bound_min) / 2
        for i in range(int(max_it / 2)):
            xi = mid + (i + 0.5) * interval
            add = f(xi) * interval
            result += add
            if abs(add) < result * 0.00001:
                break
        for i in range(int(max_it / 2)):
            xi = mid - (i + 0.5) * interval
            add = f(xi) * interval
            result += add
            if abs(add) < abs(result) * 0.00001:
                break
        return result

    def iterate_f_pdf_r(self, start: int, stop: int) -> Tuple[List[int], List[float]]:
        """Get r PDF."""
        pool = futures.ProcessPoolExecutor(128)
        future: List[futures.Future] = []
        for i in range(stop - start):
            future.append(pool.submit(execute_f_pdf_r, (self), (start+i)))
        result_x = [0] * (stop - start)
        result_y = [0.0] * (stop - start)
        for i in range(stop - start):
            futures.wait([future[i]])
            result_y[i] = future[i].result()
            result_x[i] = start + i
            print(f'Future {i} completed!')
        return result_x, result_y

    def iterate_gen(self, x_points, execute_func, name_index: int) -> None:
        """Generate iterate."""
        pool = futures.ProcessPoolExecutor(128)
        future: List[futures.Future] = []
        for i, p_i in enumerate(x_points):
            future.append(pool.submit(execute_func, (self), p_i))
        for i in range(len(x_points)):
            futures.wait([future[i]])
            result_y = future[i].result()
            print('Future ' + str(i) + ' completed!')
            self._write_csv(name_index, i, result_y)

    def _init_csv(self, sizes: List[int]) -> List[Any]:
        """Initialize the CSV."""
        with open(self.file_name, 'a', encoding='utf-8') as f:
            csv_writer = csv.writer(f, delimiter=',')
            csv_writer.writerow([])
            data_lines = self.model_data.to_csv_lines()
            for line in data_lines:
                csv_writer.writerow(line)
            # Prepare data places:
            intervals = self.model_data.get_intervals()
            print(intervals)
            names = ('T_0^n', 'T_1^n', 'T_D^n', 'Phi_D^0', 'T_pi', 'R')
            is_ints = (False, False, False, False, False, True)
            result = []
            for j, n_j in enumerate(names):
                csv_writer.writerow([n_j])
                if not is_ints[j]:
                    xs = [0.0] * sizes[j]
                    ys = [-1.0] * sizes[j]
                    for i in range(sizes[j]):
                        xs[i] = i / sizes[j] * (intervals[j][1] - intervals[j][0]) + intervals[j][0]
                else:
                    xs = range(intervals[j][0], intervals[j][1]) # type: ignore
                    ys = [-1.0] * (intervals[j][1] - intervals[j][0]) # type: ignore
                csv_writer.writerow(xs)
                csv_writer.writerow(ys)
                result += [xs]
        return result

    def _write_csv(self, name_index: int, x_index: int, value: float) -> None:
        """Write to the CSV."""
        with open(self.file_name, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            number_data = int(len(lines) / 21)
        with open(self.file_name, 'w', encoding='utf-8') as f:
            for i in range(number_data - 1):
                for j in range(21):
                    f.write(lines[i*21+j])
            line_number = 5 + name_index * 3
            for i in range(line_number):
                f.write(lines[21 * (number_data - 1) + i])
            line = lines[21 * (number_data - 1) + line_number]
            els = line.split('\n')[0].split(',')
            els[x_index] = str(value)
            new_str = els[0]
            for e in els[1:]:
                new_str += ',' + e
            new_str += '\n'
            f.write(new_str)
            for i in range(line_number+1, 21):
                f.write(lines[21 * (number_data - 1) + i])

    def plot_csv(self, index: Optional[int]=None,
                 compare: Optional[List[int]]=None) -> None:
        """Plot the CSV data."""
        self._check_csv(index)
        subplots = [0, 0, 1, 2, 3, 4]
        if compare is None:
            data = self.get_csv_data(index)
            for i, d_i in enumerate(data):
                plt.subplot((max(subplots) + 1) * 100 + 11 + subplots[i])
                plt.plot(d_i[0], d_i[1])
            plt.show()
            return
        for i, c_i in enumerate(compare):
            data_i = self.get_csv_data(c_i)
            for i, d_ii in enumerate(data_i):
                plt.subplot((max(subplots) + 1) * 100 + 11 + subplots[i])
                plt.plot(d_ii[0], d_ii[1])
        plt.show()

    def _check_csv(self, index: Optional[int]=None) -> None:
        """Check the CSV."""
        data = self.get_csv_data(index)
        for j, d_j in enumerate(data):
            inter = d_j[0][1] - d_j[0][0]
            res = 0.0
            for i, _ in enumerate(d_j[0]):
                res += d_j[1][i] * inter
            print(f'Data {j}: {res}')

    def get_csv_data(self, index: Optional[int]=None) -> List[List[List[float]]]:
        """Get the stored data."""
        if index is None:
            with open(self.file_name, 'r', encoding='utf-8') as f:
                index = len(f.readlines()) / 21 - 1 # type: ignore
        assert index is not None
        with open(self.file_name, 'r', encoding='utf-8') as f:
            csv_reader = csv.reader(f, delimiter=',')
            i = 0
            graph_i = 0
            data: List[List[List[float]]] = []
            for row in csv_reader:
                if i < index * 21 + 4:
                    i += 1
                    continue
                xs = []
                if (i - index * 21 - 4) % 3 == 0:
                    xs = [float(x) for x in row]
                if (i - index * 21 - 5) % 3 == 0:
                    ys = [float(y) for y in row]
                    data.append([xs, ys])
                    graph_i += 1
                    if graph_i >= 6:
                        break
                i += 1
        return data

    def get_csv_header(self, index: Optional[int]=None) -> List[float]:
        """Get the CSV header."""
        if index is None:
            with open(self.file_name, 'r', encoding='utf-8') as f:
                index = len(f.readlines()) / 21 - 1 # type: ignore
        assert index is not None
        with open(self.file_name, 'r', encoding='utf-8') as f:
            csv_reader = csv.reader(f, delimiter=',')
            i = 0
            data: List[float] = []
            for row in csv_reader:
                if i == index * 21 + 2:
                    data = [float(x) for x in row]
                    break
                i += 1
        return data

    def full_describe(self, size: int) -> None:
        """Describe fully."""
        x_points = self._init_csv([size] * 6)
        self.iterate_gen(x_points[0], execute_f_pdf_t0, 0)
        self.iterate_gen(x_points[1], execute_f_pdf_t1, 1)
        self.approx.approx_f_pdf_td(execute_f_pdf_td_slow, self.model_data, self)
        self.iterate_gen(x_points[2], execute_f_pdf_td, 2)
        self.f_pdf_phid_nc(0, True, True)
        self.iterate_gen(x_points[3], execute_phid, 3)
        self.iterate_gen(x_points[4], execute_t_pi, 4)
        self.iterate_gen(x_points[5], execute_f_pdf_r, 5)

    def tester_now(self) -> None:
        """Test now."""
        self.full_describe(400)
        self.plot_csv()

def execute_f_pdf_td_slow(model: Model, t: float) -> float:
    """Execute PDF td."""
    return model.f_pdf_td(t, True, False)

def execute_f_pdf_r(model: Model, r: int) -> float:
    """Execute PDF r."""
    print(f'starting f_pdf_r process for {r}')
    result = model.f_pdf_r(r, True, True,
                           model.approx.f_pdf_phid_bounds, # type: ignore
                           model.approx.f_pdf_td_bounds, True) # type: ignore
    print(f'f_pdf_r process for {r} finished, result={result}')
    return result

def execute_f_pdf_t0(model: Model, t: float) -> float:
    """Execute PDF t0"""
    print(f'Starting f_pdf_t0 process for {t}')
    result = model.f_pdf_ig(t, model.model_data.n * 2 * np.pi / model.model_data.mu_dc_0,
                            (model.model_data.n * 2 * np.pi / model.model_data.sigma_dc_0)**2)
    print(f'f_pdf_t0 process for {t} finished, result={result}')
    return result

def execute_f_pdf_t1(model: Model, t: float) -> float:
    """Execute PDF t1"""
    print(f'Starting f_pdf_t1 process for {t}')
    result = model.f_pdf_ig(t, model.model_data.n * 2 * np.pi / model.model_data.mu_dc_1,
                            (model.model_data.n * 2 * np.pi / model.model_data.sigma_dc_1)**2)
    print(f'f_pdf_t1 process for {t} finished, result={result}')
    return result

def execute_f_pdf_td(model: Model, t: float) -> float:
    """Execute PDF td"""
    print(f'Starting f_pdf_td process for {t}')
    result = model.f_pdf_td(t, True, True)
    print(f'f_pdf_td process for {t} finished, result={result}')
    return result

def execute_phid(model: Model, phi: float) -> float:
    """Execute phid."""
    print(f'Starting phid process for {phi}')
    result = model.f_pdf_phid_nc(phi, True, True)
    print(f'phid process for {phi} finished, result={result}')
    return result

def execute_t_pi(model: Model, t: float):
    """Execute t_pi."""
    print(f'Starting t_pi process for {t}')
    result = integrate.quad(lambda phi: model.f_pdf_phid_nc(phi, True, True) \
                                * model.f_pdf_t_pi(t, phi, True),
                            model.approx.f_pdf_phid_bounds[0],
                            model.approx.f_pdf_phid_bounds[1])[0]
    print(f't_pi process for {t} finished, result={result}')
    return result
