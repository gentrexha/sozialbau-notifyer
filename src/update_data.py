#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import gspread as gc
import gspread_dataframe as gd
from oauth2client.service_account import ServiceAccountCredentials


def main():
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gc.authorize(creds)

    df = pd.read_csv("../data/players.csv")

    ws = client.open("OSM Transferlist").worksheet("Data")
    gd.set_with_dataframe(ws, df)

    return 0


if __name__ == "__main__":
    main()
