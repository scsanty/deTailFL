import tensorflow_federated as tff
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
import pickle

emnist_train, emnist_test = tff.simulation.datasets.emnist.load_data()
emnist_train, emnist_test
# emnist_train.client_ids
# emnist_train.element_type_structure
dtst = emnist_train.create_tf_dataset_for_client(emnist_train.client_ids[0])

dt_t = iter(dtst)
batch = []
label = []
for i in range(7):
	example = next(dt_t)
	# plt.imshow(example['pixels'], cmap='gray')
	# example['pixels'].shape
	batch.append(tf.identity(example['pixels']))
	label.append(example['label'])

label_hot = tf.one_hot(label, depth=10)

batch = tf.stack(batch)
batch.shape
# plt.imshow(batch[0], cmap='gray')
batch_flat = tf.reshape(batch, (*batch.shape,1))
batch_flat.shape

client_model = keras.models.Sequential(
	[
		keras.layers.Conv2D(64,
							(3, 3),
							activation=tf.nn.relu,
							input_shape=(28, 28, 1)
							),
		keras.layers.MaxPool2D(2, 2),
	]
)
client_opt = tf.keras.optimizers.SGD(learning_rate=0.1)

with tf.GradientTape(persistent=True) as client_tape:
	client_pred = client_model(batch_flat)
# payload_for_server = [client_pred, label]
# ---------------------------------
server_opt = tf.keras.optimizers.SGD(learning_rate=0.1)

server_model = keras.models.Sequential([
					keras.layers.Conv2D(64, (3, 3), activation=tf.nn.relu),
					keras.layers.MaxPool2D(2, 2),
					keras.layers.Flatten(),
					keras.layers.Dense(128, activation=tf.nn.relu),
					keras.layers.Dense(10, activation=tf.nn.softmax)
])

with tf.GradientTape(persistent=True) as server_tape:
	server_tape.watch(client_pred)
	out7 = server_model(client_pred)
	cost = tf.keras.losses.SparseCategoricalCrossentropy()(label, out7)

server_gradients = server_tape.gradient(cost, server_model.trainable_weights)
server_opt.apply_gradients(zip(server_gradients, server_model.trainable_weights))

final_server_gradient = server_tape.gradient(cost, client_pred)
# payload_for_client = [final_server_gradient]
# ------------------------------------------------------------------------------
client_gradients = client_tape.gradient(client_pred,
										client_model.trainable_weights,
										output_gradients=final_server_gradient)
client_opt.apply_gradients(zip(client_gradients, client_model.trainable_weights))
