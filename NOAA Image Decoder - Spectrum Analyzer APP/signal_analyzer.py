import threading
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal.windows import get_window
import scipy.signal as signal
import struct

class SIGNAL_ANALYZER(threading.Thread):
    def __init__(self, IQ_queue, figure, ax, fft_frame):
        super(SIGNAL_ANALYZER, self).__init__()
        self.IQ_queue = IQ_queue
        self.buffer_size = 5000
        self.adc_resolution = 2**14           # Adc 12 bit, (2^12) - 1 = 4095
        self.adc_reference_voltage = 3.3    # Adc reference voltage = 3.3 [V]

        self.fft_frame = fft_frame
        self.time = np.linspace(0,100,self.buffer_size)
        self.amplitude_time = np.linspace(-3.4,3.4,self.buffer_size)
        self.freqs = np.linspace(0,25,4096)
        self.amplitude_db = np.linspace(-100,0,4096)

        self.fig,self.ax=figure,ax
        self.fig.subplots_adjust(top=0.9, bottom=0.15, left=0.07, right=0.93)
        self.line_time, = ax[0].plot(self.time, self.amplitude_time, '#2596be', linewidth=0.7)
        self.line_freq, = ax[1].plot(self.freqs, self.amplitude_db, '#2596be', linewidth=0.5)

        self.ax[0].set_title('Time-Domain IQ Signal',color='White')
        self.ax[0].set_xlim(0,100)
        self.ax[0].set_ylim(-3.3,3.3)
        self.ax[0].set_xlabel('Time [ms]', color='white')
        self.ax[0].set_ylabel('Amplitude [V]', color='white')
        self.ax[0].tick_params(axis='x', colors='white')
        self.ax[0].tick_params(axis='y', colors='white')
        self.ax[0].spines['bottom'].set_color('#2c2c2c')  # Set the color of the bottom spine
        self.ax[0].spines['bottom'].set_linestyle('--')
        self.ax[0].spines['bottom'].set_linewidth(0.5)
        self.ax[0].spines['top'].set_color('#2c2c2c')  # Set the color of the top spine
        self.ax[0].spines['top'].set_linestyle('--')
        self.ax[0].spines['top'].set_linewidth(0.5)
        self.ax[0].spines['right'].set_color('#2c2c2c')  # Set the color of the right spine
        self.ax[0].spines['right'].set_linestyle('--')
        self.ax[0].spines['right'].set_linewidth(0.5)
        self.ax[0].spines['left'].set_color('#2c2c2c')  # Set the color of the left spine
        self.ax[0].spines['left'].set_linestyle('--')
        self.ax[0].spines['left'].set_linewidth(0.5)
        self.ax[0].grid(color='#2c2c2c', linestyle='--', linewidth=0.5)



        self.ax[1].set_title('Power Spectrum', color='White')
        self.ax[1].set_xlim(0, 26)
        self.ax[1].set_ylim(-150,0)
        self.ax[1].set_xticks(np.arange(0, 26, 2))
        self.ax[1].set_xlabel('Frequency [KHz]', color='white')
        self.ax[1].set_ylabel('Power [dBm]', color='white')
        self.ax[1].tick_params(axis='x', colors='white')
        self.ax[1].tick_params(axis='y', colors='white')
        self.ax[1].spines['bottom'].set_color('#2c2c2c')   # Set the color of the bottom spine
        self.ax[1].spines['bottom'].set_linestyle('--')
        self.ax[1].spines['bottom'].set_linewidth(0.5)
        self.ax[1].spines['top'].set_color('#2c2c2c')      # Set the color of the top spine
        self.ax[1].spines['top'].set_linestyle('--')
        self.ax[1].spines['top'].set_linewidth(0.5)
        self.ax[1].spines['right'].set_color('#2c2c2c')    # Set the color of the right spine
        self.ax[1].spines['right'].set_linestyle('--')
        self.ax[1].spines['right'].set_linewidth(0.5)
        self.ax[1].spines['left'].set_color('#2c2c2c')     # Set the color of the left spine
        self.ax[1].spines['left'].set_linestyle('--')
        self.ax[1].spines['left'].set_linewidth(0.5)
        self.ax[1].grid(color='#2c2c2c', linestyle='--', linewidth=0.5)
        plt.tight_layout()
        self.animation_run = True
    def init_plot(self):
        """

        :param

        :return:
        """
        self.line_time.set_data(self.time, self.amplitude_time)

        self.line_freq.set_data(self.freqs, self.amplitude_db)
        return self.line_time, self.line_freq,

    def update_plot(self,frame):
        """

        :param

        :return:
        """

        if self.animation_run:

            I_samples,Q_samples = self.adc_to_voltage()
            #I_samples, Q_samples =self.filter_signal(I_samples,Q_samples)
            IQ_signal_no_dc = I_samples + 1j * Q_samples

            # IQ_signal_no_dc = self.remove_dc_offset(IQ_signal)
            IQ_amplitude = np.abs(IQ_signal_no_dc)

            spectrum_dbm = self.power_spectrum_dbm(IQ_signal_no_dc)


            self.line_time.set_data(self.time, IQ_amplitude)



            self.line_freq.set_data(self.freqs, spectrum_dbm)

            return self.line_time, self.line_freq,

        if not self.animation_run:
            return []  # Return an empty list if animation is not running

    def adc_to_voltage(self):
        """

        :param

        :return:
        """

        samples = self.IQ_queue.get()
        samples = samples * (self.adc_reference_voltage * 2) / self.adc_resolution

        I_samples = samples[0::2]

        Q_samples = samples[1::2]

        return I_samples -(-0.0246170654296875), Q_samples -(-0.09522618896484375)


    def power_spectrum_dbm(self, IQ_signal):
        """

        :param

        :return:
        """

        IQ_signal = np.concatenate((IQ_signal, np.zeros(3192)), 0)
        window = get_window('hamming', 8192)
        windowed_signal = IQ_signal * window
        IQ_FFT = np.fft.fftshift(np.fft.fft(windowed_signal, 8192) / 8192)  # normalized FFT of signal
        spectrum_dbm = 10 * np.log10((abs(IQ_FFT)**2) * 1000 / 50)

        return spectrum_dbm[4096:8192]

    def stop(self):
        """

        :param

        :return:
        """
        self.animation_run=False
        plt.close(self.fig)  # Close the figure
        self.join()


