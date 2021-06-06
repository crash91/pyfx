from tensorflow import keras
from tensorflow.keras import layers


""" Model Setup """
td_blocksize = 1024
ir_length = 1024
output_size = td_blocksize + ir_length - 1  # "valid" conv length
# time domain
input_samples = keras.Input(shape=(None, td_blocksize), name="samples")
x = layers.Conv1D(64, 3, activation="relu")(input_samples)
x = layers.Conv1D(64, 3, activation="relu")(x)
output_samples = layers.Conv1D(output_size, 3, activation="relu")(x)

model_td = keras.Model(inputs=input_samples,
                       outputs=output_samples, name="ir_learn")
model_td.summary()

# TODO - freq domain?


# choose model
model = model_td
# model = model_fd

""" Training """
model.compile(
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    optimizer=keras.optimizers.RMSprop(),
    metrics=["accuracy"],
)

# history = model.fit(get_samples(1024), epochs=2, steps_per_epoch=200)

""" Save Model """
# model.save("./ir_learn")
