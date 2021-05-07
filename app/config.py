import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    dataset_path: str = os.path.join('static', 'dataset')
    tmp_dir: str = "tmp"


settings = Settings()