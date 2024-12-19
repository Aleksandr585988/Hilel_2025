
import logging

GLOBAL_CONFIG = {
    "feature_a": True,
    "feature_b": False,
    "max_retries": 3
}


class Configuration:
    def __init__(self, updates, validator=None):
        """Context manager for temporarily modifying the global configuration."""

        self.updates = updates
        self.validator = validator

        self.original_config = None

    def __enter__(self):

        """Enter the context: Apply the configuration updates."""

        self.original_config = GLOBAL_CONFIG.copy()
        GLOBAL_CONFIG.update(self.updates)
        logging.info(f"Configuration updates: {self.updates}")

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the context: Restore the original configuration and handle validation or exceptions."""

        if self.validator and not self.validator(GLOBAL_CONFIG):
            logging.error(f"Configuration validation failed: {self.validator(GLOBAL_CONFIG)}")

        GLOBAL_CONFIG.clear()
        GLOBAL_CONFIG.update(self.original_config)

        logging.info(f"Configuration restored")
        return False


def validate_config(config: dict) -> bool:
    if config["max_retries"] < 0:
        return False
    return True


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    logging.info(f"Initial GLOBAL_CONFIG: {GLOBAL_CONFIG}")

    # Example 1: Successful configuration update
    try:
        with Configuration({"feature_a": False, "max_retries": 5}):
            logging.info(f"Inside context: {GLOBAL_CONFIG}")

    except Exception as e:
        logging.error(f"Error: {e}")
    logging.info(f"After context: {GLOBAL_CONFIG}", )

    # Example 2: Configuration update with validation failure
    try:
        with Configuration({"feature_a": "invalid_value", "max_retries": -1}, validator=validate_config):
            logging.info("This should not be printed if validation fails.")
    except Exception as e:
        logging.error(f"Caught exception: {e}")
    logging.info(f"After failed context: {GLOBAL_CONFIG}")
