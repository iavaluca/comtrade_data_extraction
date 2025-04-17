from collections import namedtuple
import io
import logging
import os
from contextlib import redirect_stdout
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from typing import Union
import unicodedata
from codes.functions.getData import getData, checkStatus
from codes.settings import config

def get_session_with_retries():
    """
    Create a requests session with retry logic.
    """
    session = requests.Session()
    retries = Retry(
        total=5,  # Number of retries
        backoff_factor=1,  # Delay between retries (e.g., 1s, 2s, 4s, etc.)
        status_forcelist=[500, 502, 503, 504],  # Retry on these HTTP status codes
    )
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session

def normalize_folder_name(name):
    """
    Normalize folder names to remove special characters.
    """
    return unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')

def getFolder(folder: str) -> str:
    """
    Create a directory in the current path if it doesn't exist, and return its normalized path.
    """
    normalized_folder = normalize_folder_name(folder)
    path = os.path.join(os.getcwd(), normalized_folder)
    os.makedirs(path, exist_ok=True)
    logging.info(f"{path} is ready for data storage.")
    return path

def getPeriod(frequency: str, years: list, months: Union[None, list]) -> list:
    """
    Generate time periods for API requests based on frequency.
    """
    if frequency == "M":
        try:
            time = [",".join([f"{year}{m:02}" for m in months]) for year in years]
        except TypeError:
            raise AttributeError(f"Invalid months parameter: {months}. Please input valid numbers.")
    elif frequency == "A":
        time = years
    else:
        raise ValueError(f"Invalid frequency: {frequency}. Use 'M' for monthly or 'A' for annually.")
    return time


class dataAPI:
    """
    Class for interacting with the UN Comtrade API.
    """

    def __init__(self, key: str, config: dict):
        """
        Initialize the dataAPI instance.

        :param key: API subscription key (must be provided by the user).
        :param config: Configuration dictionary with parameters for the API call.
        """
        if not key:
            raise ValueError("API key is required. Please provide it in settings.py or pass it explicitly.")
        self.key = key
        self.method = config["method"]
        self.frequency = config["frequency"]
        self.countries = config["countries"]
        self.years = config["years"]
        self.months = config["months"]
        self.hscode = config["hscode"]
        self.flows = config["flows"]
        self.partners = config["partners"]
        self.period = getPeriod(frequency=self.frequency, years=self.years, months=self.months)
        self.data_path = getFolder("data")
        self.stata_files = config["stata_files"]
        self.typeCode = config["typeCode"]

    def fetch_data(self):
        """
        Fetch data from the API and store it locally.
        """
        data = []
        # Pass named tuple as reporter
        Reporter = namedtuple('Reporter', ['name','code'])
        for period in self.period:
            for country in self.countries:
                logging.info(f"Fetching data for {country} for period {period}...")
                f = io.StringIO()
                try:
                    with redirect_stdout(f):
                        request = getData(
                            method=self.method,
                            key=self.key,
                            directory=self.data_path,
                            frequency=self.frequency,
                            period=period,
                            reporter=Reporter(
                                name=country,
                                code=self.countries.get(country)
                            ),
                            stata_files=self.stata_files,
                            typeCode=self.typeCode,
                            # TODO: to reactivate
                            # flow=self.flows,
                            # partners=self.partners,
                            # hscode=self.hscode,
                        )
                    out = f.getvalue()
                    checkStatus(method=self.method, request=request, out=out)
                    logging.info(f"Data for {country} for period {period} fetched successfully.")
                except Exception as e:
                    logging.error(f"Failed to fetch data for {country} for period {period}: {e}")
        return data

    def __repr__(self):
        """
        Developer-friendly string representation.
        """
        return f"<dataAPI: method={self.method}, frequency={self.frequency}, countries={len(self.countries)}>"