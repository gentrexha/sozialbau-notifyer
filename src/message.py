#!/usr/bin/env python
# -*- coding: utf-8 -*-
import fbchat
import logging
import os
import pandas as pd
from dotenv import find_dotenv, load_dotenv
from pathlib import Path
from update_data import preprocess_data
import glob


def main():
    logger = logging.getLogger(__name__)
    new, top = analyze_data()
    print(f"New players on the Transferlist: \n {new}")
    print(f"Top players on the Transferlist: \n {top}")
    # send_msg(f"New players on the Transferlist: \n {new}")
    # send_msg(f"Top players on the Transferlist: \n {top}")
    return 0


def find_new_players() -> pd.DataFrame:
    df_new = pd.read_csv("../data/players.csv")
    old_players = glob.glob("../data/players_*.csv")
    df_old = pd.read_csv(old_players[-2])
    df = df_new[~df_new['name'].isin(df_old['name'])]
    return df


def find_top_players(top: int = 5) -> pd.DataFrame:
    df = pd.read_csv("../data/players.csv")
    df = preprocess_data(df)
    df.sort_values(["possible profit"], inplace=True, ascending=False)
    return df.head(top)


def analyze_data():
    new_players = find_new_players()
    top_players = find_top_players()
    return (
        new_players.to_string(index=False),
        top_players.to_string(index=False),
    )


def send_msg(message):
    users = [os.environ.get("users").split(",")]
    client = fbchat.Client(os.environ["fb-username"], os.environ["fb-password"])
    for i in range(len(users)):
        name = users[i]
        friends = client.searchForUsers(name)  # return a list of names
        friend = friends[0]
        sent = client.sendMessage(message, thread_id=friend.uid)
        if sent:
            print("Message sent successfully!")


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[1]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
