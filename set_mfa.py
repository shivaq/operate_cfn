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

##################
# configure config file
##################
Config = configparser.ConfigParser()
Config._interpolation = configparser.ExtendedInterpolation()


def get_cfg():
    """Check custom config files"""
    logger.debug("get_cfg is called")

    home = Path.home()
    custom_cfg_path = home / 'operate_cfn' / 'aws.ini'

    if not custom_cfg_path.exists():
        logger.error('{0} is not exist. Please create it.'.format(custom_cfg_path))
        sys.exit(1)

    return custom_cfg_path


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

# TODO: Check Win or posix


def select_profile():
    """provide profile selection to user input"""

    sections = Config.sections()
    str_profile = "profile"
    profiles = []

    # extract profile from sections
    for section in sections:
        logger.debug(section)
        if section.startswith(str_profile):
            profiles.append(section)

    print("Selectable profiles")
    # present profile number and name
    for profile in profiles:
        print(str(profiles.index(profile) + 1) + ") " + profile[len(str_profile) + 1:])

    while True:
        profile_num = input("Input the number of the profile and ENTER.  ")
        if 1 <= int(profile_num) <= len(profiles):
            print("Thank you.")
            break
        else:
            print("wrong number")

    selected_profile = profiles[int(profile_num) - 1][len(str_profile) + 1:]
    print("You selected {}.".format(selected_profile))
    return selected_profile


# get a config file
Config.read(get_cfg())

select_profile()

# print("Print options: {}".format(Config.options("default")))
# print("Print value: {}".format(Config.get("production", "test")))
# print("Print value: {}".format(Config.get("SectionThree", "Charlie")))

# input("Which account do you use?")
