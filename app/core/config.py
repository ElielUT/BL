from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Config(BaseSettings):
    allowed:list[str] = Field(..., alias="ALLOWED.ORIGINS")
    supabase_url:str = Field(..., alias="SUPABASE_URL")
    supabase_key:str = Field(default="public", alias="SUPABASE_KEY")
    supabase_usuario:str = Field(..., alias="SUPABASE_USUARIO")
    supabase_alumno:str = Field(..., alias="SUPABASE_ALUMNO")
    supabase_asesor:str = Field(..., alias="SUPABASE_AESOSOR")
    supabase_asesoria:str = Field(..., alias="SUPABASE_ASESORIA")
    supabase_materia:str = Field(..., alias="SUPABASE_MATERIA")
    supabase_imparte:str = Field(..., alias="SUPABASE_IMPARTE")
    supabase_toma:str = Field(..., alias= "SUPABASE_TOMA")
    supabase_horario:str = Field(..., alias="SUPABASE_HORARIO")

    model_config = SettingsConfigDict(
        env_file= ".env",
        env_file_encoding="utf-8",
        extra="ignore"#El valor por default es "forbid"
    )

config = Config()