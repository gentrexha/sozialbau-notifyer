#!/bin/python
# -*- coding: utf-8 -*-
import logging
import os
import pandas as pd
from dotenv import find_dotenv, load_dotenv
from pathlib import Path
from update_data import preprocess_data
import glob
import requests


def main():
    logger = logging.getLogger(__name__)
    new, top, last_update = analyze_data()
    send_telegram_msg(f"New players on the Transferlist: \n\n {new}")
    send_telegram_msg(f"Top players on the Transferlist: \n\n {top}")
    send_telegram_msg(f"Last update: {last_update}")
    logger.info("Sent messages!")
    return 0


def find_new_players() -> (pd.DataFrame, str):
    df_new = pd.read_csv(project_dir / "data/players.csv")
    df_new = preprocess_data(df_new)
    old_players = glob.glob(project_dir.resolve().__str__() + "/data/players_*.csv")
    old_players.sort()
    df_old = pd.read_csv(old_players[-2])
    df_old = preprocess_data(df_old)
    df = df_new[~df_new["name"].isin(df_old["name"])]
    df = df.sort_values(["rating"], ascending=False)
    return df, old_players[-1][-19:-4]


def find_top_players(top: int = 5) -> pd.DataFrame:
    df = pd.read_csv(project_dir / "data/players.csv")
    df = preprocess_data(df)
    df.sort_values(["profit"], inplace=True, ascending=False)
    return df.head(top)


def analyze_data():
    new_players, last_update = find_new_players()
    top_players = find_top_players()
    return (
        new_players.to_string(
            index=False, columns=["name", "age", "rating", "price"], justify="right"
        ),
        top_players.to_string(
            index=False, columns=["name", "age", "rating", "price", "profit"], justify="right"
        ),
        last_update,
    )


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
