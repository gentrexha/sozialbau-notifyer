#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import pandas as pd
import gspread as gc
from pathlib import Path
from gspread_dataframe import set_with_dataframe
from gspread_formatting.dataframe import format_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials


def main():
    # use creds to create a client to interact with the Google Drive API
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "client_secret.json", scope
    )
    client = gc.authorize(creds)

    df = pd.read_csv("../data/players.csv")

    # Preprocess
    preprocess_data(df)

    ws = client.open("OSM Transferlist").worksheet("Data")
    set_with_dataframe(ws, df)
    # format_with_dataframe(ws, df, include_column_header=True)

    return 0


def preprocess_data(df):
    df["price"] = df["price"].apply(lambda x: x[:-1])
    df["value"] = df["value"].apply(lambda x: x[:-1])
    cols = ["age", "attack", "def", "overall", "price", "value"]
    df[cols] = df[cols].apply(pd.to_numeric, errors="coerce", axis=1)

    df["main_position_skill"] = df.apply(
        lambda row: row["attack"]
        if row["position"] == "Forward"
        else (row["overall"] if row["position"] == "Midfielder" else row["def"]),
        axis=1,
    )
    df["possible_sell_price"] = df.apply(
        lambda row: row["value"] * 2.5
        if row["main_position_skill"] < 80 or row["value"] < 9
        else row["value"] * 1.5,
        axis=1,
    )
    df["possible_profit"] = df.apply(
        lambda row: row["value"] * 2.5 - row["price"]
        if row["main_position_skill"] < 80 or row["value"] < 9
        else row["value"] * 1.5 - row["price"],
        axis=1,
    )


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[1]

    main()
