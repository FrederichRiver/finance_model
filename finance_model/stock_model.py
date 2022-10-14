#!/usr/bin/python3
import datetime
import pandas as pd
import requests
from dev_global.env import TIME_FMT
from libutils.network import RandomHeader
from lxml import etree
from pandas import DataFrame
from requests.models import HTTPError
from sqlalchemy import select
from sqlalchemy.orm import Session
from libsql_utils.model.stock import get_formStock, formStockManager


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


def get_stock_data(session: Session, stock_code: str, kwindow=[5, 10, 20]) -> DataFrame:
    col_name = ['trade_date', 'close', 'high', 'low', 'open', 'amplitude', 'volume', 'adjust']
    formStock = get_formStock(stock_code)
    query = select(
        formStock.trade_date,
        formStock.close_price,
        formStock.high_price,
        formStock.low_price,
        formStock.open_price,
        formStock.amplitude,
        formStock.volume,
        formStock.adjust_factor
        )
    result = session.execute(query).fetchmany(40)
    df =  DataFrame(result, columns=col_name)
    if df is not None:
        df.set_index('trade_date', inplace=True)
        for i in kwindow:
            df[f"MA{i}"] = df['close'].rolling(i).mean()
    return df