from pydantic import BaseSettings


class Settings(BaseSettings):
    dataset_path: str = "dataset"    
    tmp_dir: str = "tmp"


settings = Settings()