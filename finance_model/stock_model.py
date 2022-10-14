#!/usr/bin/python3
import datetime
import pandas as pd
import requests
from dev_global.env import TIME_FMT
from libutils.network import RandomHeader
from lxml import etree
from pandas import DataFrame
from requests.models import HTTPError


def get_html_object(url: str, HttpHeader: dict) -> etree.HTML:
    """
    Translate a http response into a etree.HTML object
    """
    response = requests.get(url, headers=HttpHeader, timeout=3)
    if response.status_code == 200:
        # setting encoding
        response.encoding = response.apparent_encoding
        html = etree.HTML(response.text)
    elif response.status_code == 304:
        html = None
    else:
        html = None
        raise HTTPError(f"Status code: {response.status_code} for {url}")
    return html


def get_excel_object(url: str) -> DataFrame:
    """
    Translate a excel object from http url into a DataFrame object.
    """
    df = pd.read_excel(url)
    return df


class SpiderModel(object):
    """
    
    """
    def __init__(self) -> None:
        # date format: YYYY-mm-dd
        self._Today = datetime.date.today().strftime(TIME_FMT)
        # date format: YYYYmmdd
        self._today = datetime.date.today().strftime('%Y%m%d')
        # self.TAB_STOCK_MANAGER = "stock_manager"
        self._Header = RandomHeader()

    @property
    def httpHeader(self) -> dict:
        return self._Header()

    @property
    def Today(self) -> str:
        """
        Format: 1983-01-22
        """
        self._Today = datetime.date.today().strftime(TIME_FMT)
        return self._Today

    @property
    def today(self) -> str:
        """
        Format: 19830122
        """
        self._today = datetime.date.today().strftime('%Y%m%d')
        return self._today
