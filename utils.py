import os

from tensorflow import keras


TMP_DIR = 'tmp/'

def get_model(file_data: bytes, filename: str):
    path = os.path.join(TMP_DIR, filename)
    print(path)
    with open(path, "wb") as f:
        f.write(file_data)

    model = keras.models.load_model(path)
    os.remove(path)

    return model


    
