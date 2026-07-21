import logging

from credit_pipeline.logging_config import configure_logging


def test_configure_logging_sets_up_a_handler_and_level():
    root_logger = logging.getLogger()
    original_handlers = list(root_logger.handlers)
    original_level = root_logger.level

    try:
        root_logger.handlers.clear()

        configure_logging(level=logging.DEBUG)

        assert root_logger.level == logging.DEBUG
        assert len(root_logger.handlers) >= 1
    finally:
        root_logger.handlers.clear()
        root_logger.handlers.extend(original_handlers)
        root_logger.setLevel(original_level)
