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

class AwsLogin():

    ##################
    # configure config file
    ##################
    Config = configparser.ConfigParser()
    Config._interpolation = configparser.ExtendedInterpolation()


    def __init__(self):

        # get a config file
        self.Config.read(self.get_cfg())
        self.ask_profile()


    def get_cfg(self):
        """Check custom config files"""
        logger.debug("get_cfg is called")
        home = Path.home()
        custom_cfg_path = home / 'operate_cfn' / 'aws.ini'

        if not custom_cfg_path.exists():
            logger.error('{0} is not exist. Please create it.'.format(custom_cfg_path))
            sys.exit(1)

        return custom_cfg_path

    def ask_profile(self):

        # Ask user to select profile number
        print("You use iam user {}".format(
            self.Config.get(self.select_profile(), "profile")))
        # print("Print value: {}".format(Config.get("SectionThree", "Charlie")))
        # \
        # input("Which account do you use?")



    # TODO: Get an MFA token from an argument

    # TODO: Get a role to switch from an argument

    # TODO: Check if the mfa token is int

    # TODO: Check if the mfa is longer than 6

    # TODO: get session token

    # TODO: Set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN, AWS_SECURITY_TOKEN on environment variables

    # TODO: Set AWS_SDK_LOAD_CONFIG=true

    # TODO: Set AWS_PROFILE

    # TODO: AWS_DEFAULT_REGION

    # TODO: Check Win or posix


    def select_profile(self):
        """provide profile selection to user input"""

        sections = self.Config.sections()
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
                print("Thank you.\n")
                break
            else:
                print("wrong number")

        selected_profile = profiles[int(profile_num) - 1]
        print("You selected {}.\n".format(selected_profile))
        return selected_profile

    # def get_profile_section():

aws_login = AwsLogin()

