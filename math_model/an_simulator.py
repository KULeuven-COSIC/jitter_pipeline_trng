"""This module contains stochastic model simulation capabilities."""
from typing import Callable
import numpy as np
from scipy.stats import norm # type: ignore

class Simulator:
    """The stochastic model simulator class."""

    def __init__(self, f_noise: float, per_dc_0: float, per_dc_1: float,
                 per_vdl_0: float, per_vdl_1: float, n: int=1, verbose: bool=False,
                 dc_noise_factor: float=1, nb_int: int=1000):
        self.f_noise = f_noise
        self.mu_dc_0 = 2 * np.pi / per_dc_0
        self.sigma_dc_0 = np.sqrt(self.f_noise * dc_noise_factor) * self.mu_dc_0
        self.mu_dc_1 = 2 * np.pi / per_dc_1
        self.sigma_dc_1 = np.sqrt(self.f_noise * dc_noise_factor) * self.mu_dc_1
        self.mu_vdl_0 = 2 * np.pi / per_vdl_0
        self.sigma_vdl_0 = np.sqrt(self.f_noise) * self.mu_vdl_0
        self.mu_vdl_1 = 2 * np.pi / per_vdl_1
        self.sigma_vdl_1 = np.sqrt(self.f_noise) * self.mu_vdl_1
        self.n = n
        self.verbose = verbose
        self.nb_int = nb_int # Should be even

    def f_pdf_ig(self, x: float, mu: float, la: float) -> float:
        """Get inverse Gaussian PDF."""
        if x == 0:
            return 0
        return np.sqrt(la / 2 / np.pi / (x**3)) * np.exp(-(la * (x - mu)**2) / (2 * mu**2 * x))

    def _get_max_ig_bound(self, mu: float, la: float, prec: float=1e-3) -> float:
        """Get the upper bound for the inverse Gaussian PDF."""
        result = np.power(la / 2 / np.pi / prec**2, 1 / 3)
        if mu / la < 1e-4:
            result = min(result, mu + 4 * np.sqrt(mu**3 / la))
        return result

    def _get_min_ig_bound(self, mu: float, la: float) -> float:
        """Get the lower bound for the inverse Gaussian PDF."""
        if mu / la < 1e-4:
            return max(mu - 4 * np.sqrt(mu**3 / la), 0)
        return 0

    def _integrate(self, f: Callable[[float], float], start: float, stop: float) -> float:
        """Perform an integration of f."""
        if (stop - start) / self.nb_int > 1e-1:
            print(f'Warning, integration precision is low: {start} {stop}')
        h = (stop - start) / self.nb_int
        result = 0.0
        for i in range(1, int(self.nb_int / 2)):
            result += 2 * f(start + h * 2 * i)
        for i in range(1, int(self.nb_int / 2 + 1)):
            result += 4 * f(start + h * (2 * i - 1))
        result += f(start) + f(stop)
        result *= h / 3
        return result

    def _differentiate(self, f: Callable[[float], float], x: float,
                       delta: float=1e-12) -> float:
        """Differentiate f at x."""
        return (f(x + delta / 2) - f(x - delta / 2)) / delta

    def f_pdf_t0(self, t: float) -> float:
        """PDF for T0."""
        return self.f_pdf_ig(t, self.n * 2 * np.pi / self.mu_dc_0,
                             (self.n * 2 * np.pi / self.sigma_dc_0)**2)

    def f_pdf_t1(self, t: float) -> float:
        """PDF for T1."""
        return self.f_pdf_ig(t, self.n * 2 * np.pi / self.mu_dc_1,
                             (self.n * 2 * np.pi / self.sigma_dc_1)**2)

    def _inner_p(self, int_end: float) -> float:
        """Generate inner P integral."""
        int_start = self._get_min_ig_bound(self.n * 2 * np.pi / self.mu_dc_0,
                                           (self.n * 2 * np.pi / self.sigma_dc_0)**2)
        return self._integrate(lambda t: self.f_pdf_t0(t), int_start, int_end) # pylint: disable=unnecessary-lambda

    def _inner_n(self, int_start: float) -> float:
        """Generate inner N integral."""
        int_end = self._get_max_ig_bound(self.n * 2 * np.pi / self.mu_dc_1,
                                         (self.n * 2 * np.pi / self.sigma_dc_1)**2)
        return self._integrate(lambda t: self.f_pdf_t1(t), int_start, int_end) # pylint: disable=unnecessary-lambda

    def _outer_p(self, t: float) -> float:
        """Generate outer P integral."""
        int_start = self._get_min_ig_bound(self.n * 2 * np.pi / self.mu_dc_1,
                                           (self.n * 2 * np.pi / self.sigma_dc_1)**2)
        int_end = self._get_max_ig_bound(self.n * 2 * np.pi / self.mu_dc_1,
                                         (self.n * 2 * np.pi / self.sigma_dc_1)**2)
        return self._integrate(lambda t1: self.f_pdf_t1(t1) * self._inner_p(t1 + t),
                               int_start, int_end)

    def _outer_n(self, t: float) -> float:
        """Generate outer N integral."""
        int_start = self._get_min_ig_bound(self.n * 2 * np.pi / self.mu_dc_0,
                                           (self.n * 2 * np.pi / self.sigma_dc_0)**2)
        int_end = self._get_max_ig_bound(self.n * 2 * np.pi / self.mu_dc_0,
                                         (self.n * 2 * np.pi / self.sigma_dc_0)**2)
        return self._integrate(lambda t0: self.f_pdf_t0(t0) * self._inner_n(t0 - t),
                               int_start, int_end)

    def f_cdf_tdn(self, t: float) -> float:
        """Get the TDn CDF."""
        mu_0 = self.n * 2 * np.pi / self.mu_dc_0
        la_0 = (self.n * 2 * np.pi / self.sigma_dc_0)**2
        mu_1 = self.n * 2 * np.pi / self.mu_dc_1
        la_1 = (self.n * 2 * np.pi / self.sigma_dc_1)**2
        if (mu_0 / la_0 < 1e-4) & (mu_1 / la_1 < 1e-4):
            mu = mu_0 - mu_1
            sigma = np.sqrt(mu_0**3 / la_0 + mu_1**3 / la_1)
            return norm.cdf(t, mu, sigma)
        print('f_cdf_tdn Gaussian approximation does not hold, '
              f'mu_0/la_0={mu_0 / la_0}, mu_1/la_1={mu_1 / la_1}')
        if t >= 0:
            return self._outer_p(t)
        return self._outer_n(t)

    def f_pdf_tdn(self, t: float) -> float:
        """Get the TDn PDF."""
        mu_0 = self.n * 2 * np.pi / self.mu_dc_0
        la_0 = (self.n * 2 * np.pi / self.sigma_dc_0)**2
        mu_1 = self.n * 2 * np.pi / self.mu_dc_1
        la_1 = (self.n * 2 * np.pi / self.sigma_dc_1)**2
        if (mu_0 / la_0 < 1e-4) & (mu_1 / la_1 < 1e-4):
            mu = mu_0 - mu_1
            sigma = np.sqrt(mu_0**3 / la_0 + mu_1**3 / la_1)
            return norm.pdf(t, mu, sigma)
        print('f_pdf_tdn Gaussian approximation does not hold, '
              f'mu_0/la_0={mu_0 / la_0}, mu_1/la_1={mu_1 / la_1}')
        return self._differentiate(lambda ti: self.f_cdf_tdn(ti), t) # pylint: disable=unnecessary-lambda

    def f_pdf_tvdl0(self, t: float, n: int=1) -> float:
        """Get the TVDL0 PDF."""
        return self.f_pdf_ig(t, n * 2 * np.pi / self.mu_vdl_0,
                             (n * 2 * np.pi / self.sigma_vdl_0)**2)

    def f_pdf_tvdl1(self, t: float, n: int=1) -> float:
        """Get the TVDL1 PDF."""
        return self.f_pdf_ig(t, n * 2 * np.pi / self.mu_vdl_1,
                             (n * 2 * np.pi / self.sigma_vdl_1)**2)

    def _inner_tda(self, int_end: float) -> float:
        """Generate inner TDa integral."""
        int_start = self._get_min_ig_bound(2 * 2 * np.pi / self.mu_vdl_0,
                                           (2 * 2 * np.pi / self.sigma_vdl_0)**2)
        return self._integrate(lambda t: self.f_pdf_tvdl0(t, 2), int_start, int_end)

    def f_cdf_tda(self, t: float) -> float:
        """Get the TDa CDF."""
        mu_0 = self.n * 2 * np.pi / self.mu_dc_0
        la_0 = (self.n * 2 * np.pi / self.sigma_dc_0)**2
        mu_1 = self.n * 2 * np.pi / self.mu_dc_1
        la_1 = (self.n * 2 * np.pi / self.sigma_dc_1)**2
        mu_vdl_0 = 2 * 2 * np.pi / self.mu_vdl_0
        la_vdl_0 = (2 * 2 * np.pi / self.sigma_vdl_0)**2
        mu = mu_0 - mu_1
        sigma = np.sqrt(mu_0**3 / la_0 + mu_1**3 / la_1)
        if (mu_0 / la_0 < 1e-4) & (mu_1 / la_1 < 1e-4) & (mu_vdl_0 / la_vdl_0 < 1.2e-4):
            return norm.cdf(t, mu_0 - mu_1 + mu_vdl_0,
                            np.sqrt(mu_0**3 / la_0 + mu_1**3 / la_1 + mu_vdl_0**3 / la_vdl_0))
        print('f_cdf_tda Gaussian approximation does not hold, '
              f'mu_dc_0/la_dc_0={mu_0 / la_0}, mu_dc_1/la_dc_1={mu_1 / la_1}, '
              f'mu_vdl_0/la_vdl_0={mu_vdl_0 / la_vdl_0}')
        int_start = mu - 4 * sigma
        int_end = mu + 4 * sigma
        return self._integrate(lambda ti: self.f_pdf_tdn(ti) * self._inner_tda(t - ti),
                               int_start, int_end)

    def f_pdf_tda(self, t: float) -> float:
        """Get the TDa PDF."""
        mu_dc_0 = self.n * 2 * np.pi / self.mu_dc_0
        la_dc_0 = (self.n * 2 * np.pi / self.sigma_dc_0)**2
        mu_dc_1 = self.n * 2 * np.pi / self.mu_dc_1
        la_dc_1 = (self.n * 2 * np.pi / self.sigma_dc_1)**2
        mu_vdl_0 = 2 * 2 * np.pi / self.mu_vdl_0
        la_vdl_0 = (2 * 2 * np.pi / self.sigma_vdl_0)**2
        if (mu_dc_0 / la_dc_0 < 1e-4) & (mu_dc_1 / la_dc_1 < 1e-4) & (mu_vdl_0 / la_vdl_0 < 1.2e-4):
            return norm.pdf(t, mu_dc_0 - mu_dc_1 + mu_vdl_0,
                            np.sqrt(mu_dc_0**3 / la_dc_0 + mu_dc_1**3 / la_dc_1 \
                                    + mu_vdl_0**3 / la_vdl_0))
        else:
            print('f_pdf_tda Gaussian approximation does not hold, '
                  f'mu_dc_0/la_dc_0={mu_dc_0/la_dc_0}, mu_dc_1/la_dc_1={mu_dc_1/la_dc_1}, '
                  f'mu_vdl_0/la_vdl_0={mu_vdl_0/la_vdl_0}')
            return self._differentiate(lambda ti: self.f_cdf_tda(ti), t) # pylint: disable=unnecessary-lambda

    def f_pdf_phi_vdl1_c_tda(self, phi: float, tda: float) -> float:
        """Get Phi_VDL1 PDF conditioned on TDa."""
        return norm.pdf(phi, self.mu_vdl_1 * tda, np.sqrt(self.sigma_vdl_1**2 * tda))

    def f_pdf_phi_vdl1_j_tda(self, phi: float, tda: float) -> float:
        """Get joint PDF Phi_VDL1 and TDa."""
        return self.f_pdf_phi_vdl1_c_tda(phi, tda) * self.f_pdf_tda(tda)

    def f_pdf_phi_vdl1(self, phi: float) -> float:
        """Get the Phi_VDL1 PDF."""
        mu_dc_0 = self.n * 2 * np.pi / self.mu_dc_0
        la_dc_0 = (self.n * 2 * np.pi / self.sigma_dc_0)**2
        mu_dc_1 = self.n * 2 * np.pi / self.mu_dc_1
        la_dc_1 = (self.n * 2 * np.pi / self.sigma_dc_1)**2
        mu_vdl_0 = 2 * 2 * np.pi / self.mu_vdl_0
        la_vdl_0 = (2 * 2 * np.pi / self.sigma_vdl_0)**2
        mu = mu_dc_0 - mu_dc_1 + mu_vdl_0
        sigma = np.sqrt(mu_dc_0**3 / la_dc_0 + mu_dc_1**3 / la_dc_1 + mu_vdl_0**3 / la_vdl_0)
        return self._integrate(lambda t: self.f_pdf_phi_vdl1_j_tda(phi, t),
                               mu - 5 * sigma, mu + 5 * sigma)

    def f_pdf_jit_dc_cnt(self, cnt: int) -> float:
        """Get the JIT DC count PDF."""
        old_nb_int = self.nb_int
        self.nb_int = 100
        result = self._integrate(lambda phi: self.f_pdf_phi_vdl1(phi), # pylint: disable=unnecessary-lambda
                                 2 * np.pi * (cnt - 1), 2 * np.pi * cnt)
        self.nb_int = old_nb_int
        return result

    def f_pdf_phi_d0_c_tdn(self, phi: float, t: float) -> float:
        """Get Phi_D0 PDF conditioned on TDn."""
        if t > 0:
            return norm.pdf(phi, -self.mu_vdl_1 * t, np.sqrt(self.sigma_vdl_1**2 * t))
        return norm.pdf(phi, -self.mu_vdl_0 * t, np.sqrt(-self.sigma_vdl_0**2 * t))

    def f_cdf_tpi_c_phi_d0(self, t: float, phi: float) -> float:
        """Get Tpi CDF conditioned in Phi_D0."""
        if t >= 0:
            mu_d = self.mu_vdl_0 - self.mu_vdl_1
            sigma_d = np.sqrt(self.sigma_vdl_0**2 + self.sigma_vdl_1**2)
            return 1 - norm.cdf((np.pi - mu_d * t - phi % np.pi) / (sigma_d * np.sqrt(t))) \
                + norm.cdf(-(mu_d * t + phi % np.pi) / (sigma_d * np.sqrt(t)))
        return 0

    def f_pdf_tpi_c_phi_d0(self, t: float, phi: float) -> float:
        """Get Tpi PDF conditioned in Phi_D0."""
        if t > 0:
            mu_d = self.mu_vdl_0 - self.mu_vdl_1
            sigma_d = np.sqrt(self.sigma_vdl_0**2 + self.sigma_vdl_1**2)
            return norm.pdf((np.pi - mu_d * t - (phi % np.pi)) / (sigma_d * np.sqrt(t))) \
                   * (mu_d * t + np.pi - (phi % np.pi)) / (2 * sigma_d * t * np.sqrt(t)) \
                   - norm.pdf((-mu_d * t - (phi % np.pi)) / (sigma_d * np.sqrt(t))) \
                   * (mu_d * t - (phi % np.pi)) / (2 * sigma_d * t * np.sqrt(t))
        return 0

    def f_cdf_r_c_phi_d0_tdn(self, r: int, phi: float, t: float) -> float:
        """Get R CDF conditioned on Phi_D0 and TDn."""
        if t > 0:
            return self.f_cdf_tpi_c_phi_d0((2 * np.pi * r + phi) / (self.mu_vdl_1), phi)
        return self.f_cdf_tpi_c_phi_d0((2 * np.pi * r) / (self.mu_vdl_1), phi)

    def f_pdf_r_c_phi_d0_tdn(self, r: int, phi: float, t: float) -> float:
        """Get R PDF conditioned on Phi_D0 and TDn."""
        if r == 0:
            return self.f_cdf_r_c_phi_d0_tdn(0, phi, t)
        return self.f_cdf_r_c_phi_d0_tdn(r, phi, t) - self.f_cdf_r_c_phi_d0_tdn(r - 1, phi, t)

    def f_pdf_r_j_phi_d0_tdn(self, r: int, phi: float, t: float) -> float:
        """Get joint PDF R, Phi_D0 and TDn."""
        return self.f_pdf_r_c_phi_d0_tdn(r, phi, t) * self.f_pdf_phi_d0_c_tdn(phi, t) \
               * self.f_pdf_tdn(t)

    def _inner_r(self, r: int, t: float) -> float:
        """Generate inner R integral."""
        if t > 0:
            mu = -self.mu_vdl_1 * t
            sigma = np.sqrt(self.sigma_vdl_1**2 * t)
        else:
            mu = -self.mu_vdl_0 * t
            sigma = np.sqrt(-self.sigma_vdl_0**2 * t)
        int_start = mu - 5 * sigma
        int_end = mu + 5 * sigma
        return self._integrate(lambda phi: self.f_pdf_r_j_phi_d0_tdn(r, phi, t), int_start, int_end)

    def f_pdf_r(self, r: int) -> float:
        """Get R PDF."""
        mu_dc_0 = self.n * 2 * np.pi / self.mu_dc_0
        la_dc_0 = (self.n * 2 * np.pi / self.sigma_dc_0)**2
        mu_dc_1 = self.n * 2 * np.pi / self.mu_dc_1
        la_dc_1 = (self.n * 2 * np.pi / self.sigma_dc_1)**2
        mu_tdn = mu_dc_0 - mu_dc_1
        sigma_tdn = np.sqrt(mu_dc_0**3 / la_dc_0 + mu_dc_1**3 / la_dc_1)
        int_start = mu_tdn - 5 * sigma_tdn
        int_end = mu_tdn + 5 * sigma_tdn
        return self._integrate(lambda t: self._inner_r(r, t), int_start, int_end)

    def p_1(self) -> float:
        """Get 1 probability."""
        xs = [0]
        ys = [self.f_pdf_r(xs[0])]
        while abs(1 - sum(ys)) > 1e-4:
            xs += [xs[-1] + 1]
            ys += [self.f_pdf_r(xs[-1])]
            if self.verbose:
                print(sum(ys))
                print(xs, ys)
        if self.verbose:
            print(f'xs: {xs}')
            print(f'ys: {ys}')
        result = 0.0
        for i, x_i in enumerate(xs):
            if x_i % 2 == 1:
                result += ys[i]
        return result
