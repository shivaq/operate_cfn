#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import sys
import configparser
from logging import getLogger, StreamHandler, FileHandler, Formatter, DEBUG, INFO
from logging.handlers import RotatingFileHandler

##################
# configure logging
##################
logger = getLogger(__name__)
logger.setLevel(INFO)
# create console handler
ch = StreamHandler()
ch.setLevel(INFO)
# create file handler
rfh = RotatingFileHandler(
    'operate_cfn.log', maxBytes=10485760, backupCount=1)
rfh.setLevel(DEBUG)
# create formatter and add it to the handlers
formatter = Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
rfh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(rfh)
logger.propagate = False

# TODO: set custom config file

# TODO: Check existence of custom config file

# TODO: Get an mfa arn from custom config file

# TODO: get a config file from ~/.aws/config

# TODO: Get profile from an argument

# TODO: Get an MFA token from an argument

# TODO: Get a role to switch from an argument

# TODO: Use default profile and role only specify mfa code

# TODO: Check if the profile exists

# TODO: Check if the mfa token is int

# TODO: Check if the mfa is longer than 6

# TODO: get session token

# TODO: Set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN, AWS_SECURITY_TOKEN on environment variables

# TODO: Set AWS_SDK_LOAD_CONFIG=true

# TODO: Set AWS_PROFILE

# TODO: AWS_DEFAULT_REGION
