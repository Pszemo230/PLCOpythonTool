#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import logging.handlers
from importlib import reload
from logging.config import dictConfig

import pandas

from common_config.common_config import LOG_TO_FILE_ENABLED

logger = logging.getLogger(__name__)

DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
}


def configure_logging(logfile_path):
    """
    Initialize logging defaults for Project.

    :param logfile_path: logfile used to the logfile
    :type logfile_path: string

    This function does:

    - Assign INFO and DEBUG level to logger file handler and console handler

    """
    logging.shutdown()
    reload(logging)

    dictConfig(DEFAULT_LOGGING)

    pandas.options.display.float_format = '{:.4f}'.format

    default_formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] [%(funcName)s():%(lineno)s] "
        "[PID:%(process)d TID:%(thread)d] %(message)s",
        "%d/%m/%Y %H:%M:%S")

    file_handler = logging.handlers.RotatingFileHandler(logfile_path, maxBytes=1485760, backupCount=300,
                                                        encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    file_handler.setFormatter(default_formatter)
    console_handler.setFormatter(default_formatter)

    logging.root.setLevel(logging.NOTSET)
    if LOG_TO_FILE_ENABLED: logging.root.addHandler(file_handler)
    logging.root.addHandler(console_handler)
