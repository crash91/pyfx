import numpy as np
from scipy.signal import fftconvolve, resample
import soundfile as sf

class BlockProcessor():
    """
    Block-wise processing class
    """

    def __init__(self, ir_filename: str, fs: int, blocksize: int):
        ir, ir_fs = sf.read(ir_filename)
        print(f"Loaded IR {ir_filename}")
        # if ir_fs != fs: # TODO
        #     ir = resample(ir, blocksize*fs)

        self.ir = np.expand_dims(ir, axis=1)
        self.fs = fs
        self.blocksize = blocksize

        buf_len = int(np.ceil((len(self.ir) + self.blocksize - 1) / self.blocksize)) * self.blocksize
        self.buffer = np.zeros((buf_len, 1))

    def convolve_ir_block(self, input_block: np.ndarray, output_block: np.ndarray, frames, time, status) -> np.ndarray:
        if status:
            print(status)

        # TODO code here is iffy with dims, works currently for my scarlett solo with input index 1 as the actual guitar jack
        output_block.fill(0)
        inp = np.expand_dims(input_block[:, 1], axis=1)

        y = fftconvolve(inp, self.ir)

        # add first block of buffer from last block to generate output signal
        output = y[:self.blocksize] + self.buffer[:self.blocksize]
        output_block[:, 1] = np.squeeze(output)
        # shift buffer
        self.buffer = np.roll(self.buffer, -self.blocksize)
        self.buffer[-self.blocksize:] = 0

        # add overlap signal to the buffer
        overlap = len(y) - self.blocksize
        # print(f"overlap is {overlap}, buffer shape {self.buffer[:overlap].shape}, y shape {y[self.blocksize:].shape}")
        self.buffer[:overlap] += y[self.blocksize:]
