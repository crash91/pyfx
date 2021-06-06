import sounddevice as sd

# device list setup
input_devices = list()
output_devices = list()
default_input = sd.query_devices(kind='input').get('name')
default_output = sd.query_devices(kind='output').get('name')

api_dict = sd.query_hostapis()
devices_dict = sd.query_devices()

for device in devices_dict:
    if device.get('max_input_channels') > 0:
        input_devices.append(device.get('name'))
    if device.get('max_output_channels') > 0:
        output_devices.append(device.get('name'))