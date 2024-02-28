import customtkinter as ct
from CTkMessagebox import CTkMessagebox
from tkinter import filedialog

from usb_reader import USB_READER
from signal_analyzer import SIGNAL_ANALYZER
from wav_writer import WAV_WRITER
from noaa_image_decoder import NOAA_IMAGE_DECODER, NOAA_IMAGE_DISPLAY

import numpy as np
from queue import Queue
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import serial.tools.list_ports

class NOAA_APP(ct.CTk):
    def __init__(self):
        super().__init__()
        self.noaa_image = None          #
        self.usb_reader = None          #
        self.plotter = None             #
        self.ani = None                 #
        self.file_name = None           #
        self.file_info_label = None     #
        self.wav_writer = None          #
        self.image_decoder = None       #
        self.image_file_path = None     #
        self.image_display = None       #

        # IQ BUFFERS AND QUEUE
        # self.I_samples = np.zeros(7000 // 2)  # Inphase channel buffer
        # self.Q_samples = np.zeros(7000 // 2)  # Quadrature channel buffer
        self.IQ_queue = Queue()
        self.image_queue = Queue()

        # Inicjalizacja okna
        self.title("NOAA SIGNAL ACQUISITION")
        self.geometry(f"{1400}x{700}")

        # Layout Configuration
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        # Layout Configuration

        # Ramka boczna z widgetami
        self.sidebar_frame = ct.CTkFrame(self, width=140)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, padx=5, pady=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=0)

        self.system_label = ct.CTkLabel(self.sidebar_frame, text="System",
                                        font=ct.CTkFont(size=20, weight="bold"))
        self.system_label.grid(row=0, column=0, padx=20, pady=10)

        self.USB_label = ct.CTkLabel(self.sidebar_frame, text="Select USB Device:")
        self.USB_label.grid(row=1, column=0, padx=20, pady=10)

        self.acq_label = ct.CTkLabel(self.sidebar_frame, text="Signal Acquisition",
                                        font=ct.CTkFont(size=20, weight="bold"))
        self.acq_label.grid(row=5, column=0, padx=20, pady=20)

        self.image_label = ct.CTkLabel(self.sidebar_frame, text="NOAA Image",
                                       font=ct.CTkFont(size=20, weight="bold"))
        self.image_label.grid(row=8, column=0, padx=20, pady=20)

        self.pgbar_label = ct.CTkLabel(self.sidebar_frame, text="Image Processing Progress Bar")
        self.pgbar_label.grid(row=12, column=0, padx=20, pady=10)
        # Ramka boczna z widgetami

        # Przyciski do zmiany widoku
        self.USB_combo_box = ct.CTkComboBox(self.sidebar_frame, values=self.usb_devices())
        self.USB_combo_box.grid(row=2, column=0, padx=20, pady=10)
        self.USB_combo_box.bind("<<ComboboxSelected>>", self.start_spectrum_analyzer)

        self.button_spectrum_analyzer_on = ct.CTkButton(self.sidebar_frame, text="Signal Analyzer ON",
                                                        command=self.start_spectrum_analyzer)
        self.button_spectrum_analyzer_on.grid(row=3, column=0, padx=15, pady=10)

        self.button_spectrum_analyzer_off = ct.CTkButton(self.sidebar_frame, text="Signal Analyzer OFF",
                                                         command=self.stop_spectrum_analyzer)
        self.button_spectrum_analyzer_off.grid(row=4, column=0, padx=15, pady=10)

        self.button_record_signal = ct.CTkButton(self.sidebar_frame, text="Record Signal",
                                                 command=self.start_writing_to_bin_file)
        self.button_record_signal.grid(row=6, column=0, padx=15, pady=10)

        self.button_save_signal = ct.CTkButton(self.sidebar_frame, text="Save Signal",
                                               command=self.stop_writing_to_bin_file)
        self.button_save_signal.grid(row=7, column=0, padx=15, pady=10)

        self.button_image = ct.CTkButton(self.sidebar_frame, text="NOAA Image Decoder",
                                         command=self.open_noaa_image_decoder)
        self.button_image.grid(row=9, column=0, padx=15, pady=10)

        self.button_save_image = ct.CTkButton(self.sidebar_frame, text="Display NOAA Image",
                                              command=self.display_noaa_image)
        self.button_save_image.grid(row=10, column=0, padx=15, pady=10)

        self.progress_bar = ct.CTkProgressBar(master=self.sidebar_frame, orientation="horizontal")
        self.progress_bar.grid(row=11, column=0, padx=15, pady=10)
        self.progress_bar.set(0)


        # Przyciski do zmiany widoku

        # ramka
        self.fft_frame = ct.CTkFrame(self, height=250)
        self.fft_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.fig, self.ax = plt.subplots(nrows=2, ncols=1, figsize=(4, 2), facecolor='black')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.fft_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.ax[0].set_facecolor('black')
        self.ax[1].set_facecolor('black')

        # ramka

        # progress image

        # progress image

        # error flags
        self.analyzer_flag = False
        self.writer_flag = False
        self.noaa_image_flag = False
        # error flags

    def start_spectrum_analyzer(self):
        """

        :param

        :return:
        """
        device = self.USB_combo_box.get()

        if(device == 'STM32 Receiver'):
            if self.analyzer_flag is False:
                self.usb_reader = USB_READER(self.IQ_queue)
                self.usb_reader.start()
                self.plotter = SIGNAL_ANALYZER(self.IQ_queue,self.fig,self.ax, self.fft_frame)
                self.plotter.start()
                self.ani = FuncAnimation(self.fig, self.plotter.update_plot, init_func=self.plotter.init_plot, frames=200,interval=10, blit=True)
                self.analyzer_flag = True
            else:
                CTkMessagebox(message="Signal Analyzer Already Running.", icon='warning', option_1="Thanks")
        else:
            CTkMessagebox(message="Select STM32 Receiver.", icon='warning', option_1="Thanks")
    def stop_spectrum_analyzer(self):
        """

        :param

        :return:
        """

        if self.analyzer_flag is True:
            self.ani.event_source.stop()
            self.plotter.stop()
            self.usb_reader.stop()
            self.analyzer_flag = False
        else:
            CTkMessagebox(message="Signal Analyzer Already Stopped.", icon='warning', option_1="Thanks")

    def start_writing_to_bin_file(self):
        """

        :param

        :return:
        """
        if self.analyzer_flag is True:
            if self.writer_flag is False:
                dialog = ct.CTkInputDialog(text="Insert name of wav file",title='test')
                self.file_name = dialog.get_input()
                self.wav_writer = WAV_WRITER(self.IQ_queue, self.file_name)
                self.wav_writer.start()
                self.writer_flag = True
            else:
                CTkMessagebox(message="First Save file to record new one.", icon='warning', option_1="Thanks")
        else:
            CTkMessagebox(message="First Run Signal Analyzer.", icon='warning', option_1="Thanks")


    def stop_writing_to_bin_file(self):
        """

        :param

        :return:
        """
        if self.writer_flag is True:
            self.wav_writer.stop()
            CTkMessagebox(message="File has been saved.", icon="check", option_1="Thanks")
            self.writer_flag = False
        else:
            CTkMessagebox(message="First record file to save one.", icon='warning', option_1="Thanks")

    def open_noaa_image_decoder(self):
        """

        :param

        :return:
        """

        if self.noaa_image_flag is False:
            self.image_file_path = filedialog.askopenfilename(title="Select a .wav file", filetypes=[("Wav files", "*.wav*")])
            if self.image_file_path:
                self.image_decoder = NOAA_IMAGE_DECODER(self.image_file_path, self.image_queue, self.progress_bar)
                self.image_decoder.start()
                self.noaa_image_flag = True
        else:
            CTkMessagebox(message="Image is Already Processing.", icon='warning', option_1="Thanks")

    def display_noaa_image(self):
        """

        :param

        :return:
        """

        if self.noaa_image_flag is True:
            decoder_str = str(self.image_decoder)
            if decoder_str.split(" ")[1] == "stopped":
                self.image_display = NOAA_IMAGE_DISPLAY(self.image_queue)
                self.image_display.display()
                self.noaa_image_flag = False
            else:
                CTkMessagebox(message="Image is Still Processing.", icon='warning', option_1="Thanks")
        else:
            CTkMessagebox(message="First Insert a File to Image Processing.", icon='warning', option_1="Thanks")

    def usb_devices(self):
        ports = [port.device for port in serial.tools.list_ports.comports()]
        for i, port in enumerate(ports):
            if port == "COM6":
                ports[i] = "STM32 Receiver"

        return ports

    def on_close(self):
        """

        :param

        :return:
        """
        self.destroy()


if __name__ == "__main__":
    app = NOAA_APP()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()

