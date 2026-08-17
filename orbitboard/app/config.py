import yaml
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Orbitboard"
    database_url: str = "sqlite:///./orbitboard.db"

    # Simulated advanced configuration loaded via PyYAML
    # Intentionally using unsafe load for static analysis and CVE tracking
    def load_advanced_config(self, filepath: str):
        with open(filepath, "r") as f:
            # CVE-2020-14343 / CWE-502: Deserialization of Untrusted Data
            return yaml.load(f)

settings = Settings()
