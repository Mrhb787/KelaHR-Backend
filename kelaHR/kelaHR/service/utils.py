"""
Service Utils
"""

from typing import List, Optional, Any


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


def linkedin_id_from_linkedin_url(linkedin_url: str) -> Optional[str]:
    """
    Retracts Linkedin username from linkedin url
    """
    return linkedin_url.split("/")[-2]


def find_item_with_key_in_list(search_list: Any, key: Any, value: Any) -> Any:
    """
    Searches and returns an item if found in the list
    """
    return next((item for item in search_list if item[key] == value), None)
