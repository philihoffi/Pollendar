import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

DATA_DIR = Path("data")
CONFIG_FILE = DATA_DIR / "config.json"


def _ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> dict:
    _ensure_data_dir()
    if not CONFIG_FILE.exists():
        return {}
    try:
        return json.loads(CONFIG_FILE.read_text())
    except (json.JSONDecodeError, OSError) as e:
        logger.error("Failed to load config: %s", e)
        return {}


def save_config(data: dict):
    _ensure_data_dir()
    CONFIG_FILE.write_text(json.dumps(data, indent=2))


def get_summary_channel_id() -> int | None:
    return load_config().get("summary_channel_id")


def set_summary_channel_id(channel_id: int):
    config = load_config()
    config["summary_channel_id"] = channel_id
    save_config(config)
