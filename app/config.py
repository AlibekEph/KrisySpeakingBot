# app/config.py
import configparser
from pathlib import Path

class Settings:
    def __init__(self, config_path: Path):
        self._config = configparser.ConfigParser()
        self._config.read(config_path)
        self.telegram = self._config['telegram']
        self.llm = self._config['llm']
        self.logging = self._config['logging']

config = Settings(Path(__file__).parent.parent / 'settings.ini')
