"""
Service Utils
"""

from typing import List


def list_to_string(list_data: List[str], seperator: str = ",") -> str:
    """
    Converts the list of string to string with provided seperator
    """
    final_str: str = ""
    for data in list_data:
        final_str += data + seperator
    return final_str[:-1]


def string_to_list(input_string: str, seperator: str = ",") -> List[str]:
    """
    Converts the string with given seperator to list of strings
    """
    final_list: List[str] = input_string.split(sep=seperator)
    return final_list
