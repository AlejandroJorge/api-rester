from pydantic import BaseModel


class AppConfig(BaseModel):
    verbose: bool = False


app_config = AppConfig()
