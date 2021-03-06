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

















# layer1 = keras.layers.Conv2D(
# 					64,
# 					(3, 3),
# 					activation=tf.nn.relu,
# 					input_shape=(28, 28)
# )
# layer2 = keras.layers.MaxPool2D(2, 2)
# layer3 = keras.layers.Conv2D(64, (3, 3), activation=tf.nn.relu)
# layer4 = keras.layers.MaxPool2D(2, 2)
# layer5 = keras.layers.Flatten()
# layer6 = keras.layers.Dense(128, activation=tf.nn.relu)
# layer7 = keras.layers.Dense(10, activation=tf.nn.softmax)

# with tf.GradientTape(persistent=True) as t7:
# 	out1 = layer1(batch_flat)
# 	out2 = layer2(out1)
# 	out3 = layer3(out2)
# 	out4 = layer4(out3)
# 	out5 = layer5(out4)
# 	out6 = layer6(out5)
# 	out7 = layer7(out6)
# 	cost = tf.keras.losses.SparseCategoricalCrossentropy()(label, out7)
# out1.shape
# out2.shape
# out3.shape
# out4.shape
# out5.shape
# out6.shape
# out7.shape
#
# # dC_dw_l7 = t7.gradient(cost, layer7.weights)
# # dC_dw_l6 = t7.gradient(cost, layer6.weights)
# # dC_dw_l3 = t7.gradient(cost, layer3.weights)
# # dC_dw_l1 = t7.gradient(cost, layer1.weights)
#
# dz_dw_l7 = t7.gradient(out7, layer7.weights)
# dC_dz_l7 = t7.gradient(cost, out7)
#
# dC_dw_l7 = (tf.transpose(out6)@dC_dz_l7)	# dz_dw*dC_dz = out6.T*dC_dz
# dC_db_l7 = tf.math.reduce_mean(dC_dz_l7, axis=0)
#
# opt = tf.keras.optimizers.SGD(learning_rate=0.1)
# opt.apply_gradients(zip([dC_dw_l7, dC_db_l7], layer7.weights))
#
# dC_dw_l6 = (tf.transpose(out5)@dC_dz_l7)@tf.transpose(layer7.weights[0])
# dC_db_l6 = tf.math.reduce_mean((layer7.weights[0]@tf.transpose(dC_dz_l7)), axis=1)
#
#
# opt.apply_gradients(zip([dC_dw_l6, dC_db_l6], layer6.weights))
#
#
#
# out3.shape
# layer3.weights[0].shape
#
# out2.shape
# layer6.weights[0].shape
# layer7.weights[0].shape
# dC_dz_l7.shape
#
#
# (tf.transpose(out5)@dC_dz_l7)
