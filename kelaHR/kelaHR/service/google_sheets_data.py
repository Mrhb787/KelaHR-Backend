"""
Google Sheets DB service
"""

from typing import List, Dict, TypedDict, Optional
from pathlib import Path
from google.oauth2.service_account import Credentials
from gspread.client import Client
from gspread.spreadsheet import Spreadsheet
from gspread.worksheet import Worksheet
import gspread

from .utils import list_to_string, string_to_list


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
SERVICE_ACCOUNT_FILE = Path(__file__).resolve().parent / "kela-hr-credentials.json"
GOOGLE_SHEET_KEY = "1onSPo1o0LVSV27H_yNPZW2SKFw0gdj03B6ztbkPHOFQ"
WORKSHEET_ID = 1421025962


class TransformDataStructure(TypedDict):
    id: int
    linkedin_id: str
    email: List[str]
    phoneno: List[str]


def tranform_raw_data_to_dict(
    worksheet_raw_data: List[List[str]],
) -> Dict[str, TransformDataStructure]:
    """
    Tranforms the raw data recieved from worksheet to a useful
    indexed dictionary for fast operations
    """
    final_structure: Dict[str, TransformDataStructure] = {}
    worksheet_raw_data = worksheet_raw_data[1:]
    row_count = 2
    for row in worksheet_raw_data:
        linkedin_id: str = row[0]
        final_structure[linkedin_id] = TransformDataStructure(
            id=row_count,
            linkedin_id=linkedin_id,
            email=string_to_list(row[1]),
            phoneno=string_to_list(row[2]),
        )
        row_count += 1
    return final_structure


def tranform_raw_data_to_list(
    worksheet_raw_data: List[List[str]],
) -> List[TransformDataStructure]:
    """
    Tranforms the raw data recieved from worksheet to a useful
    indexed dictionary for fast operations
    """
    final_structure: List[TransformDataStructure] = []
    worksheet_raw_data = worksheet_raw_data[1:]
    row_count = 2
    for row in worksheet_raw_data:
        linkedin_id: str = row[0]
        final_structure.append(
            TransformDataStructure(
                id=row_count,
                linkedin_id=linkedin_id,
                email=string_to_list(row[1]),
                phoneno=string_to_list(row[2]),
            )
        )
        row_count += 1
    return final_structure


class GoogleWorksheetDB:
    def __init__(self) -> None:
        self.client: Client = self.connect_database
        self.worksheet: Worksheet = self.get_worksheet
        self.worksheet_data: List[List[str]] = self.get_worksheet_data
        self.worksheet_data_dict: Dict[str, TransformDataStructure] = (
            tranform_raw_data_to_dict(self.worksheet_data)
        )
        self.worksheet_data_list: List[TransformDataStructure] = (
            tranform_raw_data_to_list(self.worksheet_data)
        )

    @property
    def connect_database(self) -> Client:
        """
        Google OAuth2.0 Client Generation
        """
        credentials: Credentials = Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=SCOPES,
        )
        connection: Client = gspread.authorize(credentials)
        return connection

    @property
    def refresh_database_connection(self) -> Client:
        """
        Google OAuth2.0 Client ReGeneration

        In case the connetion is timedout or due to network problems get disconnected
        a connection refresh will happen to establish a fresh client generation.
        """
        return self.connect_database

    @property
    def get_worksheet(self) -> Worksheet:
        """
        Gets the worksheet that is used as Database
        """
        sheet: Spreadsheet = self.client.open_by_key(GOOGLE_SHEET_KEY)
        worksheet: Worksheet = sheet.get_worksheet_by_id(WORKSHEET_ID)
        return worksheet

    @property
    def get_worksheet_data(self) -> List[List[str]]:
        """
        Gets all the data from the Worksheet
        """
        return self.worksheet.get_all_values()

    def is_existing_data(self, key: str) -> Optional[TransformDataStructure]:
        """
        Checks and returns if the data is already
        existing in the sheet data or not for given key
        """
        if self.worksheet_data_dict.get(key, None) is not None:
            return self.worksheet_data_dict[key]
        return None

    def add_data(self, data: TransformDataStructure) -> bool:
        """
        Adds new data to the worksheet
        """
        if not self.is_existing_data(key=data["linkedin_id"]):
            row = [
                data["linkedin_id"],
                list_to_string(data["email"]),
                list_to_string(data["phoneno"]),
            ]
            self.worksheet.append_row(row)
            return True
        return False

    def update_data(self, data: TransformDataStructure) -> bool:
        """
        Updates the data to the worksheet
        """
        row = [
            data["linkedin_id"],
            list_to_string(data["email"]),
            list_to_string(data["phoneno"]),
        ]
        cell_range: str = f"A{data['id']}:C{data['id']}"
        try:
            self.worksheet.update(range_name=cell_range, values=[row])
            return True
        except Exception as exc:  # pylint: disable=broad-except
            print(exc)
        return False
