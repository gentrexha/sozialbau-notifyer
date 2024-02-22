#!/bin/python
# -*- coding: utf-8 -*-
import logging
import os
import pandas as pd
from dotenv import find_dotenv, load_dotenv
from pathlib import Path
import glob
import requests


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', None)


def main():
    logger = logging.getLogger(__name__)
    new, last_update = find_new_flats()

    if not new.empty:
        for _, row in new.iterrows():
            # Construct a message by including only selected columns
            flat_details = "\n".join([f"{col}: {row[col]}" for col in new.columns if
                                      col not in ['Lage URL', 'Location URL']])
            send_telegram_msg(f"New flat on Sozialbau.at:\n\n{flat_details}")
        # Send a message with the last update time
        send_telegram_msg(f"Last update: {last_update}")

    logger.info("Sent messages!")
    return 0


def find_new_flats() -> (pd.DataFrame, str):
    df_new = pd.read_csv(project_dir / "data/flats.csv")
    old_players = glob.glob(project_dir.resolve().__str__() + "/data/flats_*.csv")
    # get second last file to compare with last file
    df_old = pd.read_csv(old_players[-2])
    df = df_new[~df_new["Adresse"].isin(df_old["Adresse"])]
    return df, old_players[-1][-19:-4]


def send_telegram_msg(bot_message):
    bot_token = os.environ["bot_token"]
    bot_chatID = os.environ["bot_chatID"]
    send_text = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={bot_chatID}&text={bot_message}"
    response = requests.get(send_text)
    return response.json()


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[1]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
