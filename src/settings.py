from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    tg_id: int
    api_url: str
    id_instance: int
    api_token_instance: str
    phone_number: str
    bot_token: str
    start_sticker: str = "CAACAgIAAxkBAAEQCWFpRRSccMdclOer6W8j5eJyGnQnJgACWFoAAsQGyEoEWLbXXN37-DYE"
    echo_sticker: str = "CAACAgIAAxkBAAEQCWNpRRiXXk70V4JkW_v6xlOshDHBwwACjh4AAt57UEoD27hgWsI3DTYE"


settings = Settings()
