from pydantic import BaseSettings


class Settings(BaseSettings):
    """Settings."""

    url: str = "https://www.tournamentsoftware.com/sport"
    cookie_url = "https://www.tournamentsoftware.com/cookiewall/Save"
    log_level: str = "INFO"

    class Config:
        """Config."""

        env_prefix = "tsw_"
