#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import sys
import configparser
from logging import getLogger, StreamHandler, FileHandler, Formatter, DEBUG, INFO
from logging.handlers import RotatingFileHandler
import util_string
import boto3
import datetime

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
        with open(get_cfg()) as cfg:
            self.Config.read_file(cfg)

        # get value from aws.ini
        profile_section = self.ask_profile_section()
        profile = util_string.remove_quotes(
            self.Config.get(profile_section, "profile"))
        print("You use iam user {}".format(profile))
        mfa_arn = util_string.remove_quotes(
            self.Config.get(profile_section, "mfa"))
        mfa_token = self.ask_mfa_token(profile)
        role_to_switch = util_string.remove_quotes(
            self.Config.get(profile_section, "role_to_switch"))
        region = util_string.remove_quotes(
            self.Config.get(profile_section, "region"))

        # prepare session for aws
        session = boto3.session.Session(profile_name=profile)
        sts_client = session.client('sts')

        # Get session token
        token_info = sts_client.get_session_token(
            DurationSeconds=43200,  # 12 hours
            SerialNumber=mfa_arn,
            TokenCode=mfa_token
        )

        with open("tmp_token", "a") as token:
            token.write("export AWS_ACCESS_KEY_ID=" + token_info['Credentials']['AccessKeyId'] + "\n")
            token.write("export AWS_SECRET_ACCESS_KEY=" +
                        token_info['Credentials']['SecretAccessKey'] + "\n")
            token.write("export AWS_SESSION_TOKEN=" +
                        token_info['Credentials']['SessionToken'] + "\n")
            token.write("export AWS_SECURITY_TOKEN=" +
                        token_info['Credentials']['SessionToken'] + "\n")
            token.write("export AWS_SDK_LOAD_CONFIG=true\n")
            token.write("export AWS_PROFILE=" + role_to_switch + "\n")
            token.write("export AWS_DEFAULT_REGION=" + region + "\n")

        print("Please execute 'source tmp_token'")

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

        # Check if there is profile
        if not profile_list:
            logger.error("There is no profile in your aws.ini.")
            exit(1)

        input_num = self.ask_input_profile_num(str_profile, profile_list)
        selected_section = profile_list[int(input_num) - 1]
        print("You selected {}.\n".format(selected_section))
        return selected_section

    def ask_input_profile_num(self, str_profile, profile_list):
        """Ask input for profile number"""
        print("Selectable profiles")
        is_valid_number = False
        while not is_valid_number:
            is_number = False
            while not is_number:
                # present profile number and name
                for profile in profile_list:
                    print(str(profile_list.index(profile) + 1) + ") " + profile[len(str_profile) + 1:])
                input_num = input("Enter the number of the profile. ")
                # Check if input is num
                if not input_num.isdecimal():
                    print("\nYou input {}. It's {}. Enter a number.\n".format(input_num, type(input_num)))
                else:
                    # Check if input is in range of profile position
                    if 1 <= int(input_num) <= len(profile_list):
                        print("Thank you.\n")
                        return input_num
                    else:
                        print("\nYou input a wrong number.\n")

    def ask_mfa_token(self, profile):
        """Prompt user input for mfa token"""
        logger.debug("Start ask_mfa_token().")
        is_valid_number = False
        while not is_valid_number:
            is_number = False
            while not is_number:
                input_num = input(
                    "Enter MFA token for {}. ".format(profile))
                # Check if input is num
                if not input_num.isdecimal():
                    print("\nYou input {}. It's {}. Enter a number.\n".format(
                        input_num, type(input_num)))
                else:
                    return input_num


aws_login = AwsLogin()
