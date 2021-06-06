import os
from tensorflow.keras.utils import Sequence


class DataGenerator(Sequence):
    def __init__(self, data_folder, labels_folder, batch_size):
        data_list = os.listdir(data_folder)
        labels_list = os.listdir(labels_folder)

        for data in data_list:
            if data not in labels_list:
                data_list.remove(data)

        assert(len(data_list) == len(labels_list))

        self.data_list = data_list
        self.labels_list = labels_list

        self.size = len(data_list)

    def __len__(self):
        return int(self.size / self.batch_size)

    def __getitem__(self, index):
        pass



