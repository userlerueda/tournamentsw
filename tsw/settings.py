from pydantic import BaseSettings


class Settings(BaseSettings):
    """Settings."""

    url: str = "https://www.tournamentsoftware.com"
    cookie_url = "https://www.tournamentsoftware.com/cookiewall/Save"
    log_level: str = "INFO"
    draw_fixtures = {
        "65": {
            "Round 1": range(1, 64, 2),
            "Round 2": range(2, 64, 4),
            "Quarter Finals": range(4, 64, 8),
        }
    }

    class Config:
        """Config."""

        env_prefix = "tsw_"
