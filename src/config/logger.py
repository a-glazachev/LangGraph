"""
Module: config/logger.py
Description:
    This module is responsible for logger's setup
"""

import logging

import colorlog


def init_logger():
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'black',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    ))
    root.addHandler(handler)
