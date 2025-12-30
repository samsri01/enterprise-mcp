from pydantic import BaseModel

class Settings(BaseModel):
    app_name: str = "EnterpriseMCP"
    debug_mode: bool = True

settings = Settings()