import threading
import numpy as np
import wave
# from timeit import default_timer as timer
class WAV_WRITER(threading.Thread):
    def __init__(self, IQ_queue, file_name):
        super().__init__()
        self.IQ_queue = IQ_queue
        self.wav_file_path = file_name + ".wav"
        self.is_running = True
        # self.i = 0
        # self.sec = 0

    def run(self):
        """

        :param

        :return:
        """
        with wave.open(self.wav_file_path, 'w') as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2)
            wf.setframerate(50e3)

            while self.is_running:
                samples = self.IQ_queue.get()
                IQ_samples =(np.vstack((samples[1::2],samples[0::2]))).astype(np.int16)
                wf.writeframes(IQ_samples.tobytes())


    def stop(self):
        """

        :param

        :return:
        """
        self.is_running = False
        self.join()




