#!/usr/bin/env python3
# -*- coding: utf-8 -*-  
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger()
logger.setLevel(logging.NOTSET)

_handler = RotatingFileHandler('/tmp/pkuxkx.log', maxBytes=10*1024*1024,backupCount=5)
_handler.setFormatter(logging.Formatter("%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s"))
logger.addHandler(_handler)
