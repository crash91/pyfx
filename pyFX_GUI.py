import os

import PySimpleGUI as sg
import numpy as np
import sounddevice as sd
import soundfile as sf
from scipy.signal import fftconvolve
import matplotlib.pyplot as plt
""" Processing """


def process_frame(indata, outdata, frames, time, status):
    if status:
        print(status)
    outdata.fill(0)
    conv_result = fftconvolve(indata[:, 1], impulse_response, 'same')
    outdata[:, 0] = conv_result
    outdata[:, 1] = conv_result
    # outdata[:] = indata

def alert_popup(msg):
    alert = sg.Window('', [[sg.Text(msg)], [sg.OK()]],
                      element_justification='c', no_titlebar=True)
    alert.read()
    alert.close()

""" GUI setup """
sg.theme('DarkBlack')

input_devices = list()
output_devices = list()
default_input = sd.query_devices(kind='input').get('name')
default_output = sd.query_devices(kind='output').get('name')
for device in sd.query_devices():
    if device.get('max_input_channels') > 0:
        input_devices.append(device.get('name'))
    if device.get('max_output_channels') > 0:
        output_devices.append(device.get('name'))
layout = [
    [sg.Text("Input: ", size=(8, 1)), sg.Combo(input_devices, default_value=default_input, key='input_device', size=(50, 1))],
    [sg.Text("Output:", size=(8, 1)), sg.Combo(output_devices, default_value=default_output, key='output_device', size=(50, 1))],
    [sg.Input(size=(50, 1), key='ir_filename')],
    [sg.FileBrowse(target='ir_filename')],
    [sg.OK('Load IR', bind_return_key=True)]
]

window = sg.Window('pyFX', layout, element_justification='c')

while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Exit', 'Quit'):
        break

    if event == 'Load IR':
        ir_filename = values.get('ir_filename')
        if not ir_filename or not os.path.isfile(ir_filename) or not ir_filename.endswith('.wav'):
            alert_popup("Please select a valid IR file!")
        else:
            impulse_response, fs = sf.read(ir_filename)
            print(f"Loaded IR {ir_filename}")
            # plt.plot(data)
            # plt.show(block=False)

            try:
                # with sd.Stream(device=(values.get('input_device'), values.get('output_device')), callback=process_frame):
                with sd.Stream(callback=process_frame):
                    alert_popup("Click to stop streaming")
            except Exception as e:
                exit(-1)

window.close()
