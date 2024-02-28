import customtkinter as ct

import scipy.io.wavfile as wav
import numpy as np
from scipy.signal import hilbert, resample

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from scipy.signal.windows import get_window
import threading
from PIL import Image
from scipy.signal import decimate

class NOAA_IMAGE_DISPLAY(ct.CTkToplevel):
    def __init__(self, image_queue):
        super().__init__()
        self.title(" NOAA IMAGE DECODER")
        self.geometry(f"{1400}x{700}")

        self.noaa_image = None
        self.image_queue = image_queue


        # layout configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.image_label = ct.CTkLabel(self, text="NOAA Weather Satellite Received Image",
                                       font=ct.CTkFont(size=20, weight="bold"))
        self.image_label.grid(row=0, column=0, padx=15, pady=10)

        self.image_label = ct.CTkLabel(self, text="Left Channel - Visible          Right Channel - Infrared",
                                       font=ct.CTkFont(size=20, weight="bold"))
        self.image_label.grid(row=1, column=0, padx=15, pady=10)

        self.image_frame = ct.CTkFrame(self)
        self.image_frame.grid(row=8, column=0, padx=50, pady=50, sticky='nsew')
        # layout configuration

        #
        self.fig, self.ax = plt.subplots(figsize=(15, 10), facecolor='black')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.image_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.ax.set_facecolor('black')
        self.fig.subplots_adjust(top=1, bottom=0, left=0.0, right=1)
        #
    def display(self):
        """

        :param

        :return:
        """
        self.noaa_image = self.image_queue.get()
        self.ax.imshow(self.noaa_image, aspect='auto', cmap='gray')


class NOAA_IMAGE_DECODER(threading.Thread):
    def __init__(self, image_file_path, image_queue, progress_bar):
        super().__init__()

        self.file_path = image_file_path    #
        self.synchronization_sequence = np.array([0, 0, 255, 255, 0, 0, 255, 255,  #
                                                  0, 0, 255, 255, 0, 0, 255, 255,
                                                  0, 0, 255, 255, 0, 0, 255, 255,
                                                  0, 0, 255, 255, 0, 0, 0, 0, 0,
                                                  0, 0, 0]) - 128
        self.image_queue = image_queue      #
        self.progress_bar = progress_bar    #
        self.image_status = False
    def read_wav_file(self):
        """

        :param

        :return:
        """

        sample_rate,radio_signal = wav.read(self.file_path)
        IQ_signal = radio_signal[:, 0] + 1j * radio_signal[:, 1]
        window = get_window('blackmanharris', len(IQ_signal))
        t = np.linspace(0, len(IQ_signal) / sample_rate, len(IQ_signal))
        IQ_signal = IQ_signal * window * np.exp(2 * np.pi * 1j * (-4.5e3) * t)

        return IQ_signal

    def fm_demodulation(self, IQ_signal):
        """

        :param

        :return:
        """
        conjugate_product = IQ_signal[1:] * np.conj(IQ_signal[:-1])
        fm_signal = np.angle(conjugate_product)
        fm_signal = (fm_signal / max(fm_signal)) * 32767
        q = 3                                   # Calculate the decimation factor (q)
        fm_signal_dec = decimate(fm_signal, q)  # Decimate the fm signal

        return fm_signal_dec

    def apply_hilbert_transform(self, fm_signal, resample_factor=5):
        """

        :param

        :return:
        """

        fm_hilbert = np.abs(hilbert(fm_signal))
        fm_hilbert_dec = resample(fm_hilbert, len(fm_hilbert) // resample_factor)

        return fm_hilbert_dec

    def quantize(self, fm_hilbert_dec, black_point=5, white_point=95):
        """

        :param

        :return:
        """

        #  percent for upper and lower saturation
        low, high = np.percentile(fm_hilbert_dec, (black_point, white_point))

        # range adjustment and quantization
        quantized_signal = np.round((255 * (fm_hilbert_dec - low)) / (high - low)).clip(0, 255)

        return quantized_signal

    def stack_into_image(self, quantized_signal, min_row_separation=2000):
        """
        """

        # Initialize variables
        rows = [None]
        prev_corr = -np.inf
        prev_row_idx = 0

        # Iterate through the signal to stack rows
        for current_idx in range(len(quantized_signal) - len(self.synchronization_sequence)):

            # Extract a row from the signal
            current_row = []
            for x in quantized_signal[current_idx: current_idx + len(self.synchronization_sequence)]:
                current_row.append(x - 128)  # normalized to zero by -128

            # Calculate correlation between the row and the synchronization sequence
            corr_with_sequence = np.dot(self.synchronization_sequence, current_row)

            # Check if enough separation to start hunting for the next synchronization sequence
            if current_idx - prev_row_idx > min_row_separation:
                prev_corr, prev_row_idx = -np.inf, current_idx
                rows.append(quantized_signal[current_idx: current_idx + 2080])

            # If the proposed region matches the sequence better, update
            elif corr_with_sequence > prev_corr:
                prev_corr, prev_row_idx = corr_with_sequence, current_idx
                rows[-1] = quantized_signal[current_idx: current_idx + 2080]

        # Stack the rows to form the image, drop incomplete rows at the end
        noaa_image = np.vstack([row for row in rows if len(row) == 2080])
        return noaa_image

    def run(self):
        """

        :param

        :return:
        """
        self.progress_bar.start()

        IQ_signal = self.read_wav_file()
        fm_signal = self.fm_demodulation(IQ_signal)
        fm_hilbert = self.apply_hilbert_transform(fm_signal)
        quantized = self.quantize(fm_hilbert)
        noaa_image = self.stack_into_image(quantized)
        image = Image.fromarray(noaa_image)
        self.image_queue.put(image)

        self.progress_bar.stop()
        self.progress_bar.set(100)

        return



