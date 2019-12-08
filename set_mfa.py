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


def get_cfg():
    """Check custom config files"""

    logger.debug("get_cfg is called")
    home = Path.home()
    custom_cfg_path = home / 'operate_cfn' / 'aws.ini'

    if not custom_cfg_path.exists():
        logger.error('{0} is not exist. Please create it.'.format(custom_cfg_path))
        sys.exit(1)

    return custom_cfg_path


class AwsLogin:
    ##################
    # configure config file
    ##################
    Config = configparser.ConfigParser()
    Config._interpolation = configparser.ExtendedInterpolation()

    def __init__(self):

        # get a config file
        self.Config.read(get_cfg())
        profile_section = self.ask_profile_section()
        profile = self.Config.get(profile_section, "profile")

        print("You use iam user {}".format(profile))

        # self.check_mfa()
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

    def ask_profile_section(self):
        """ Prompt user selected profile """

        section_list = self.Config.sections()
        str_profile = "profile"
        profile_list = []

        # extract profile from sections
        for section in section_list:
            logger.debug(section)
            if section.startswith(str_profile):
                profile_list.append(section)

        print("Selectable profiles")
        is_valid_number = False
        while not is_valid_number:
            is_number = False
            while not is_number:
                # present profile number and name
                for profile in profile_list:
                    print(str(profile_list.index(profile) + 1) + ") " + profile[len(str_profile) + 1:])
                input_num = input("Input the number of the profile and ENTER.  ")
                if not input_num.isdecimal():
                    print("\nYou input {}. It's {}. Enter a number.\n".format(input_num, type(input_num)))
                else:
                    if 1 <= int(input_num) <= len(profile_list):
                        print("Thank you.\n")
                        is_number = True
                        is_valid_number = True
                    else:
                        print("\nYou input a wrong number.\n")

        selected_section = profile_list[int(input_num) - 1]
        print("You selected {}.\n".format(selected_section))
        return selected_section

    # def get_profile_section():


aws_login = AwsLogin()
