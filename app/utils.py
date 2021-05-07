import os
import tensorflow as tf

from tensorflow import keras
from .preprocessing import get_data
from .config import settings


def test_model(file_data: bytes, filename: str):
    path = os.path.join(settings.tmp_dir, filename)
    with open(path, "wb") as f:
        f.write(file_data)

    model = keras.models.load_model(path)
    os.remove(path)

    dataset = tf.data.experimental.load(
        settings.dataset_path,
        element_spec=(
            tf.TensorSpec(shape=(None, 64, 64, 3), dtype=tf.float64, name=None), 
            tf.TensorSpec(shape=(None,), dtype=tf.int32, name=None)
        ))
    
    model.compile(model.optimizer, model.loss, metrics='accuracy')
    _, accuracy = model.evaluate(dataset, verbose=0)
    accuracy = round(accuracy*100, 3)

    return accuracy