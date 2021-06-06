import os

import numpy as np
import soundfile as sf
import librosa
from scipy import signal
import argparse
from tqdm import tqdm
import multiprocessing as mp


def convolve_ir(impulse_response: np.ndarray, impulse_response_fs: int, in_file: str, out_file: str) -> None:
    data, fs = librosa.load(in_file, sr=impulse_response_fs) # load with resampling
    label = signal.fftconvolve(data, impulse_response)
    sf.write(out_file, label, fs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--indir', help='input directory', default='./data')
    parser.add_argument('-o', '--outdir', help='output directory', default='./labels')
    parser.add_argument('-ir', '--impulse_response', help='impulse response to convolve with', required=True)
    args = parser.parse_args()

    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)

    ir, ir_fs = librosa.load(args.impulse_response, sr=None)
    print(f"Loaded impulse response file {args.impulse_response} with samplerate {ir_fs}")

    input_files = os.listdir(args.indir)

    with mp.Pool() as pool:
        with tqdm(input_files, unit='file') as t:
            for filename in t:
                t.set_description(filename)
                pool.apply_async(convolve_ir(ir, ir_fs, os.path.join(args.indir, filename), os.path.join(args.outdir, filename)))
