import tensorflow_federated as tff
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
import pickle



emnist_train, emnist_test = tff.simulation.datasets.emnist.load_data()
emnist_train, emnist_test
emnist_train.client_ids
emnist_train.element_type_structure
dtst = emnist_train.create_tf_dataset_for_client(emnist_train.client_ids[0])

dt_t = iter(dtst)
batch = []
label = []
for i in range(10):
	example = next(dt_t)
	# plt.imshow(example['pixels'], cmap='gray')
	# example['pixels'].shape
	batch.append(tf.identity(example['pixels']))
	label.append(example['label'])

batch = tf.stack(batch)
batch.shape
plt.imshow(batch[0], cmap='gray')
batch_flat = tf.reshape(batch, (*batch.shape,1))
batch_flat.shape

out1 = keras.layers.Conv2D(	64,
							(3, 3),
							activation=tf.nn.relu,
							input_shape=(28, 28)
						)(batch_flat)
out1.shape

out2 = keras.layers.MaxPool2D(2, 2)(out1)
out2.shape

out3 = keras.layers.Conv2D(64, (3, 3), activation=tf.nn.relu)(out2)
out4 = keras.layers.MaxPool2D(2, 2)(out3)
out5 = keras.layers.Flatten()(out4)
out6 = keras.layers.Dense(128, activation=tf.nn.relu)(out5)
out7 = keras.layers.Dense(10, activation=tf.nn.softmax)(out6)


tf.keras.losses.CategoricalCrossentropy()(label, out7)


with open('filename.pickle', 'wb') as f:
	pickle.dump(out2, f, protocol=pickle.HIGHEST_PROTOCOL)
