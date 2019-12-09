#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def remove_quotes(source_str):
        "remove quotes around string"

        return_str = source_str.lstrip("'")
        return_str = return_str.rstrip("'")
        return_str = return_str.lstrip("\"")
        return_str = return_str.rstrip("\"")
        return return_str
