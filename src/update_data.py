#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import pandas as pd
import gspread as gc
from pathlib import Path
from gspread_dataframe import set_with_dataframe
from dotenv import find_dotenv, load_dotenv
from oauth2client.service_account import ServiceAccountCredentials


def main():
    logger = logging.getLogger(__name__)
    logger.info("Using credentials to interact with the Google Drive API.")
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

    logger.info("Preprocessing data.")
    df = preprocess_data(df)

    ws = client.open("OSM Transferlist").worksheet("Data")
    set_with_dataframe(ws, df)
    logger.info("Upload successful.")
    # format_with_dataframe(ws, df, include_column_header=True)

    return 0


def preprocess_data(df) -> pd.DataFrame:
    df["price"] = df["price"].apply(lambda x: x[:-1])
    df["value"] = df["value"].apply(lambda x: x[:-1])
    cols = ["age", "attack", "def", "overall", "price", "value"]
    df[cols] = df[cols].apply(pd.to_numeric, errors="coerce", axis=1)

    df["difference"] = df.apply(lambda row: row["price"] - row["value"], axis=1)
    df["rating"] = df.apply(
        lambda row: row["attack"]
        if row["position"] == "Forward"
        else (row["overall"] if row["position"] == "Midfielder" else row["def"]),
        axis=1,
    )
    df["sell"] = df.apply(
        lambda row: row["value"] * 2.5
        if row["rating"] < 80 or row["value"] < 9
        else row["value"] * 1.5,
        axis=1,
    )
    df["profit"] = df.apply(
        lambda row: row["value"] * 2.5 - row["price"]
        if row["rating"] < 80 or row["value"] < 9
        else row["value"] * 1.5 - row["price"],
        axis=1,
    )
    return df


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[1]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
