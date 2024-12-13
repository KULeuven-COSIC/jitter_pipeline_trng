"""Main ASIC readout module."""
from typing import Optional, List, Tuple, Union
from os.path import join
import time
import serial # type: ignore # pylint: disable=import-error
import matplotlib.pyplot as plt
import numpy as np

class AsicReader:
    """ASIC readout class."""

    _DEFAULT_DEV = join('/dev', 'ttyUSB1')
    _SIGNAL_NAMES = ['All 0', 'All 1', 'EXT_CLK', 'EXT_RST', 'CONF_CLK', 'CONF_IN',
                     'EXT_START', 'CONF_RST', 'DATA_OUT', 'DATA_READY', 'RO_OUT']

    def __init__(self, dev: Optional[str]=None, baud: int=115200, verbose: bool=False,
                 scope_window: int=1024):
        if dev is None:
            self.dev = AsicReader._DEFAULT_DEV
        else:
            self.dev = dev
        self.baud = baud
        self.verbose = verbose
        self.ser = serial.Serial(self.dev, self.baud)
        self.conf_ro_freq: Optional[int] = None
        self.conf_bit_cnt: Optional[int] = None
        self.nb_scope_samples: Optional[int] = None
        self.scope_window = scope_window
        self.scope_per = 0.0
        self.signals: List[int] = []
        time.sleep(1)

    def _write(self, bys: List[int]) -> None:
        """Write to the ASIC."""
        if self.verbose:
            print(bys)
        self.ser.write(bytes(bys))

    def _read(self, number: int) -> bytes:
        """Read from the ASIC."""
        data = self.ser.read(number)
        return data

    def reset_asic(self, conf: bool, asic: bool) -> None:
        """Reset the ASIC."""
        if conf & asic:
            n = 0
        elif asic:
            n = 1
        elif conf:
            n = 2
        else:
            print("no reset!")
            return
        self._write([2, n])

    def set_conf(self, bit_cnt: int, send_enable: int, dc_0: int, dc_1: int, fb: int,
                 en_high_dc: int, freq_sel: int, vdl_0: int, vdl_1: int, ro_choose: int,
                 en_high_vdl: int, ro_en: int, ro_freq: int) -> None:
        """Send configuration to ASIC."""
        if (bit_cnt < 0) | (bit_cnt > 1):
            print("bit_cnt out of range!")
            return
        if (send_enable < 0) | (send_enable > 1):
            print("send_enable out of range!")
            return
        if (dc_0 < 0) | (dc_0 >= 2**16):
            print("dc_0 out of range!")
            return
        if (dc_1 < 0) | (dc_1 >= 2**16):
            print("dc_1 out of range!")
            return
        if (fb < 0) | (fb > 1):
            print("fb out of range!")
            return
        if (en_high_dc < 0) | (en_high_dc > 1):
            print("en_high_dc out of range!")
            return
        if (freq_sel < 0) | (freq_sel >= 2**2):
            print("freq_sel out of range!")
            return
        if (vdl_0 < 0) | (vdl_0 >= 2**16):
            print("vdl_0 out of range!")
            return
        if (vdl_1 < 0) | (vdl_1 >= 2**16):
            print("vdl_1 out of range!")
            return
        if (ro_choose < 0) | (ro_choose >= 2**2):
            print("ro_choose out of range!")
            return
        if (en_high_vdl < 0) | (en_high_vdl > 1):
            print("en_high_vdl out of range!")
            return
        if (ro_en < 0) | (ro_en > 1):
            print("ro_en out of range!")
            return
        if (ro_freq < 0) | (ro_freq >= 2**3):
            print("ro_freq out of range!")
            return
        self._write([3, bit_cnt, send_enable, int(dc_0 / 256), dc_0 % 256,
                     int(dc_1 / 256), dc_1 % 256, fb, en_high_dc, freq_sel,
                     int(vdl_0 / 256), vdl_0 % 256, int(vdl_1 / 256), vdl_1 % 256,
                     ro_choose, en_high_vdl, ro_en, ro_freq])
        self.conf_ro_freq = ro_freq
        self.conf_bit_cnt = bit_cnt

    def drive_ext_start(self, times: int, interval: int) -> None:
        """Drive the external start signal."""
        if (times < 0) | (times >= 2**32):
            print("times out of range!")
            return
        if (interval < 0) | (interval >= 32):
            print("interval out of range!")
            return
        self._write([4, int(times / 256**3), int(times / 256**2)%256,
                     int(times / 256) % 256, times % 256, interval])

    def reset_buffers(self) -> None:
        """Reset the buffers."""
        self._write([5])

    def get_address(self) -> Tuple[int, int]:
        """Get current address."""
        self.reset_asic(False, True)
        self.clear_uart_buffers()
        self._write([8])
        data = self._read(4)
        data_p = [x for x in data]
        # (readAddr, writeAddr)
        return (data_p[0] * 256 + data_p[1], data_p[2] * 256 + data_p[3])

    def set_period_length(self, period_length: int, conf: bool) -> None:
        """Set the period length."""
        if (period_length < 0) | (period_length >= 32):
            print("period_length out of range!")
            return
        if conf:
            n = 0
        else:
            n = 1
        self._write([7, period_length, n])

    def clear_uart_buffers(self) -> None:
        """Clear the UART buffers."""
        while self.ser.in_waiting > 0:
            self.ser.read()

    def measure_ro_out(self, interval: int, number: int) \
        -> Optional[Union[List[float], Tuple[None, List[List[float]]]]]:
        """Measure output of RO."""
        if (interval < 0) | (interval >= 64):
            print("interval out of range!")
            return None
        if number < 0:
            print("number out of range!")
            return None
        if self.conf_ro_freq is None:
            print("conf_ro_freq not defined!")
            return None
        self.reset_asic(False, True)
        self.clear_uart_buffers()
        self._write([1, interval])
        data = self._read((number + 2) * 8)
        data_p = [x for x in data]
        data_p = data_p[8:]
        data_i = [[0.0] * number for i in range(8)]
        for shift in range(8):
            for i in range(number):
                for j in range(8):
                    data_i[shift][i] += data_p[i * 8 + j + shift] * 256**(7 - j)
                data_i[shift][i] *= 2**(4+self.conf_ro_freq)*100
                data_i[shift][i] /= 2**interval
        min_range = np.inf
        min_range_index = -1
        for shift in range(8):
            rangee = max(data_i[shift]) - min(data_i[shift])
            if rangee < min_range:
                min_range = rangee
                min_range_index = shift
        if min_range > 0:
            return data_i[min_range_index]
        for shift in range(8):
            if (data_i[shift][0] >= 50) & (data_i[shift][0] < 12800):
                return data_i[shift]
        return (None, data_i)

    def read_buffers(self, number: int) -> Optional[List[int]]:
        """Read the buffers."""
        if (number < 0) | (number >= 256**4):
            print("number out of range!")
            return None
        if self.conf_bit_cnt is None:
            print("conf_bit_cnt not defined!")
            return None
        if self.conf_bit_cnt == 0:
            if number % 2 == 1:
                print("number must be even if conf_bit_cnt equals zero!")
                return None
        if self.conf_bit_cnt == 0:
            number /= 2 # type: ignore
            number = int(number)
        self.reset_asic(False, True)
        self.clear_uart_buffers()
        self._write([6, int(number / 256**3), int(number / 256**2) % 256,
                     int(number / 256) % 256, int(number % 256)])
        data = self._read(int(number * 2))
        data_p = [x for x in data]
        if self.conf_bit_cnt == 0:
            return data_p
        data_i = [0] * number
        for i in range(number):
            for j in range(2):
                data_i[i] += data_p[i * 2 + j] * 256**(1 - j)
        return data_i

    def read_out_conf(self, conf_dc_0: int, conf_dc_1: int, conf_vdl_0: int, conf_vdl_1: int,
                      n: int=2048, verbose: bool=False, conf_freq_sel: int=0,
                      read_freq: bool=True) \
        -> Tuple[float, float, float, float, Optional[List[int]]]:
        """Read out the configured frequencies."""
        self.set_period_length(5, True)
        self.set_period_length(5, False)
        if read_freq:
            self.set_conf(1, 1, conf_dc_0, conf_dc_1, 0, 1, conf_freq_sel, conf_vdl_0,
                          conf_vdl_1, 0, 1, 1, 7)
            freq_dc_0: float = self.measure_ro_out(25, 1)[0] # type: ignore
            self.set_conf(1, 1, conf_dc_0, conf_dc_1, 0, 1, conf_freq_sel, conf_vdl_0,
                          conf_vdl_1, 1, 1, 1, 7)
            freq_dc_1: float = self.measure_ro_out(25,1)[0] # type: ignore
            self.set_conf(1, 1, conf_dc_0, conf_dc_1, 0, 0, conf_freq_sel, conf_vdl_0,
                          conf_vdl_1, 2, 1, 1, 7)
            freq_vdl_0: float = self.measure_ro_out(25,1)[0] # type: ignore
            self.set_conf(1, 1, conf_dc_0, conf_dc_1, 0, 0, conf_freq_sel, conf_vdl_0,
                          conf_vdl_1, 3, 1, 1, 7)
            freq_vdl_1: float = self.measure_ro_out(25,1)[0] # type: ignore
            if verbose:
                delta = abs(1 / freq_vdl_0 - 1 / freq_vdl_1) * 1000000
                init_diff = (-1 / freq_dc_0 + 1 / freq_dc_1) * 1000000
                if delta != 0:
                    long_run = (1 / freq_vdl_0 * 1000000 / 2 - init_diff) / delta
                else:
                    long_run = -1
                print(1 / freq_dc_0 * 1000, 1 / freq_dc_1 * 1000, 1 / freq_vdl_0 * 1000000,
                      1 / freq_vdl_1 * 1000000)
                print(f'Delta: {delta:4.1f} ps, long_run: {long_run:5.1f}, '
                      f'init_diff: {init_diff:5.1f} ps')
        else:
            freq_dc_0 = -1.0
            freq_dc_1 = -1.0
            freq_vdl_0 = -1.0
            freq_vdl_1 = -1.0
        self.set_conf(1, 1, conf_dc_0, conf_dc_1, 0, 0, conf_freq_sel, conf_vdl_0,
                      conf_vdl_1, 3, 0, 0, 7)
        self.reset_asic(False, True)
        self.reset_buffers()
        i = 0
        not_work = False
        old_address = None
        while self.get_address()[1] <= n + 64:
            i += 1
            if i == 100:
                if self.get_address()[1] != 0:
                    continue
                not_work = True
                break
            if i % 100 == 0:
                if old_address is not None:
                    if old_address == self.get_address()[1]:
                        not_work = True
                        break
                old_address = self.get_address()[1]
            time.sleep(0.01)
        if not_work:
            if verbose:
                print('Could not read CSCNT')
            return (freq_dc_0, freq_dc_1, freq_vdl_0, freq_vdl_1, None)
        a = self.read_buffers(n)
        b = np.histogram(a, bins=range(min(a), max(a)+2)) # type: ignore
        if verbose:
            plt.plot(b[1][0:len(b[1]) - 1], b[0])
            plt.plot([int(long_run)] * (max(b[0]) - min(b[0]) + 1), range(min(b[0]), max(b[0]) + 1))
            plt.plot([int(init_diff / delta)] * (max(b[0]) - min(b[0]) + 1),
                     range(min(b[0]), max(b[0]) + 1))
            plt.show()
        return (freq_dc_0, freq_dc_1, freq_vdl_0, freq_vdl_1, [x for x in a]) # type: ignore

    def wait_init(self, ti: int=40) -> None:
        """Wait for the ASIC to initialize."""
        for i in range(ti):
            print(f'Waiting to start experiment...{ti - 1 - i}')
            time.sleep(1)
        a: Tuple[float, float, float, float, Optional[List[int]]] = (0, 0, 0, 0, None)
        while a[4] is None:
            a = self.read_out_conf(0, 0, 257, 257, 1)
            time.sleep(1)
        print("Experiment started!")

    def set_scope(self, signal0: int, signal1: int, signal2: int, signal3: int,
                  trigger: int, sample_per: float, nb_samples: int) -> None:
        """
        Set the scope.
            - Signals: 0: all zero, 1: all one, 2: EXT_CLK, 3: EXT_RST, 4: CONF_CLK,
                       5: CONF_IN, 6: EXT_START, 7: CONF_RST, 8: DATA_OUT,
                       9: DATA_READY, 10: RO_OUT
            - Trigger: 0 and 1: trigger now, rest: same as signals
            - SamplePer: sample period [s]
            - nb_samples: number of samples (max 32 768)
        """
        if (signal0 < 0) | (signal0 > 10):
            print(f'signal0 out of range: {signal0}')
            return
        if (signal1 < 0) | (signal1 > 10):
            print(f'signal1 out of range: {signal1}')
            return
        if (signal2 < 0) | (signal2 > 10):
            print(f'signal2 out of range: {signal2}')
            return
        if (signal3 < 0) | (signal3 > 10):
            print(f'signal3 out of range: {signal3}')
            return
        if (trigger < 0) | (trigger > 10):
            print(f'trigger out of range: {trigger}')
            return
        if (sample_per < 10e-9) | (sample_per >= 2**32 * 10e-9):
            print(f'sample period out of range: {sample_per}')
            return
        if (nb_samples < 0) | (nb_samples > 4 * 2**13):
            print(f'Number of samples out of range: {nb_samples}')
            return
        if nb_samples % 2 != 0:
            print('Number of samples should be even')
            return
        self.scope_per = sample_per
        self.signals = [signal0, signal1, signal2, signal3]
        sample_per = int(sample_per / 10e-9 + 0.5)
        self.nb_scope_samples = nb_samples
        self._write([9, signal3, signal2, signal1, signal0, trigger,
                     int(sample_per / 256**3), int(sample_per / 256**2) % 256,
                     int(sample_per / 256) % 256, sample_per%256, int(nb_samples / 256**3),
                     int(nb_samples / 256**2) % 256, int(nb_samples / 256) % 256, nb_samples % 256])

    def _get_scope(self) -> Optional[List[int]]:
        """Get the scope data."""
        if self.nb_scope_samples is None:
            print('First setup scope by running: \'set_scope(...)\'')
            return None
        self.clear_uart_buffers()
        self._write([10])
        times = int(np.floor(self.nb_scope_samples / self.scope_window / 2))
        last_window = (int(self.nb_scope_samples / 2)) % self.scope_window
        data: List[int] = []
        for _ in range(times):
            data += self._read(self.scope_window)
        data += self._read(last_window)
        self.nb_scope_samples = None
        return data

    def plot_scope(self) -> None:
        """Plot the scoped data."""
        data = self._get_scope()
        if data is None:
            return
        s0 = []
        s1 = []
        s2 = []
        s3 = []
        t = []
        time_ = 0.0
        for d_i in data:
            for j in range(2):
                d = int(d_i / 16**(1 - j)) % 16
                s0 += [d % 2]
                s1 += [int(d / 2) % 2]
                s2 += [int(d / 4) % 2]
                s3 += [int(d / 8)]
                t += [time_]
                time_ += self.scope_per
        leg = []
        plt.plot(t, [4.5 + x for x in s0])
        leg += [self._SIGNAL_NAMES[self.signals[0]]]
        plt.plot(t, [3 + x for x in s1])
        leg += [self._SIGNAL_NAMES[self.signals[1]]]
        plt.plot(t, [1.5 + x for x in s2])
        leg += [self._SIGNAL_NAMES[self.signals[2]]]
        plt.plot(t, [0 + x for x in s3])
        leg += [self._SIGNAL_NAMES[self.signals[3]]]
        plt.legend(leg)
        plt.show()

    def reset_scope(self) -> None:
        """Reset the scope."""
        self._get_scope()

    def drive_ext_clk(self, times: int, interval: int) -> None:
        """Drive the external clock."""
        if (times < 0) | (times >= 2**32):
            print("times out of range!")
            return
        if (interval < 1) | (interval >= 32):
            print("interval out of range!")
            return
        self._write([11, int(times / 256**3), int(times / 256**2) % 256, int(times / 256) % 256,
                     times % 256, interval])

    def _jitter_manage(self, nb_cycles: int, nb_samples: int, callibrate: bool) \
        -> Tuple[List[int], List[int], List[List[int]], List[List[int]]]:
        """Manage the jitter."""
        if nb_samples > 4096 / 34:
            print('UART buffer will overflow')
        self.clear_uart_buffers()
        self._write([12, int(callibrate), int(nb_samples / 256**3), int(nb_samples / 256**2) % 256,
                     int(nb_samples / 256) % 256, nb_samples % 256, int(nb_cycles / 256**3),
                     int(nb_cycles / 256**2) % 256, int(nb_cycles / 256) % 256, nb_cycles % 256])
        expected_number_bytes = 34 * nb_samples
        last_waiting = -1
        while (self.ser.in_waiting != expected_number_bytes) \
            & (last_waiting != self.ser.in_waiting):
            last_waiting = self.ser.in_waiting
            time.sleep(0.1)
        if self.ser.in_waiting != expected_number_bytes:
            print(f'Expected {expected_number_bytes} bytes, '
                  f'but recieved only {self.ser.in_waiting}')
        answer = self._read(min(self.ser.in_waiting, expected_number_bytes))
        answer = [x for x in answer] # type: ignore
        if len(answer) != expected_number_bytes:
            for i in range(len(answer) - 1):
                if (answer[i] == 55) & (answer[i + 1] == 170):
                    answer = answer[i:]
                    break
        nb_received_samples = int(len(answer) / 34)
        cnts0 = [0] * nb_received_samples
        cnts1 = [0] * nb_received_samples
        dcs0: List[List[int]] = []
        dcs1: List[List[int]] = []
        for i in range(nb_received_samples):
            sample = answer[i * 34:i * 34 + 34]
            cnts0[i] = sample[14] * 256**3 + sample[15] * 256**2 + sample[16] * 256 + sample[17]
            cnts1[i] = sample[30] * 256**3 + sample[31] * 256**2 + sample[32] * 256 + sample[33]
            dc_raw_0 = [0] * 96
            dc_raw_1 = [0] * 96
            for j in range(12):
                dc_sample_0 = sample[13 - j]
                dc_sample_1 = sample[29 - j]
                for k in range(8):
                    dc_raw_0[j * 8 + k] = int(dc_sample_0 / 2**k) % 2
                    dc_raw_1[j * 8 + k] = int(dc_sample_1 / 2**k) % 2
            dcs0.append(dc_raw_0)
            dcs1.append(dc_raw_1)
        return (cnts0, cnts1, dcs0, dcs1)

    def jitter_callibrate(self, nb_cycles: int, nb_samples: int) \
        -> Optional[Tuple[List[int], List[int], List[List[int]], List[List[int]]]]:
        """Callibrate the jitter set-up."""
        if (nb_cycles <= 0) | (nb_cycles >= 2**32):
            print("Number cycles out of range!")
            return None
        if (nb_samples < 0) | (nb_samples >= 2**32):
            print("Number samples out of range!")
            return None
        return self._jitter_manage(nb_cycles, nb_samples, True)

    def jitter_measure(self, nb_samples: int) \
        -> Optional[Tuple[List[int], List[int], List[List[int]], List[List[int]]]]:
        """Perform the jitter measurement."""
        if (nb_samples < 0) | (nb_samples >= 2**32):
            print('Number samples out of range!')
            return None
        return self._jitter_manage(0, nb_samples, False)
