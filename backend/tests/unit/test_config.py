from src.common.config import load_yaml_config


def test_load_base_config():
    config = load_yaml_config("base.yaml")
    assert "app" in config
    assert config["app"]["name"] == "FinShield Fraud Detection Platform"