import tensorflow as tf

from preprocessing import get_data
from config import settings


def create_dataset():
    x_test, y_test = get_data()
    dataset = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(100)
    tf.data.experimental.save(dataset, settings.dataset_path)


if __name__ == '__main__':
    create_dataset()