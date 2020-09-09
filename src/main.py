#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import datetime


def get_player_data(data, text: str):
    """
    Extracts data as list from the player.text
    :param text:
    :return:
    """
    text_list = text.split("\n")
    # get all except last
    data.extend(text_list[:-1])
    data.extend(text_list[-1].split(" "))
    print(data)
    return data


def main():
    logger = logging.getLogger(__name__)
    driver = webdriver.Chrome()
    # Accept terms and conditions
    driver.get("https://en.onlinesoccermanager.com/Login?nextUrl=%2FCareer")
    driver.implicitly_wait(10)
    driver.find_element_by_class_name("custom-checkbox").click()
    driver.find_element_by_class_name("btn-new").click()

    # Login
    driver.implicitly_wait(10)
    driver.find_element_by_id("login-link").click()
    driver.implicitly_wait(10)
    try:
        driver.find_element_by_id("manager-name").send_keys(os.environ["manager-name"])
        driver.find_element_by_id("password").send_keys(os.environ["password"])
    except KeyError:
        logger.info("Please put manager-name and password in .env file.")
        return 0
    driver.find_element_by_id("login").click()

    # Choose team
    driver.implicitly_wait(10)
    driver.find_element_by_xpath("//h2[text()='Team Analyst']").click()

    # Go to Transferlist
    # TODO: Find out why the script gets stuck at the dashboard sometimes
    driver.implicitly_wait(10)
    driver.get("https://en.onlinesoccermanager.com/Transferlist")
    assert "Transfer List" in driver.title
    driver.implicitly_wait(10)
    transferlist = driver.find_element_by_id("transfer-list")
    positions = transferlist.find_elements(By.TAG_NAME, "tbody")

    df = pd.DataFrame(
        columns=["position", "name", "age", "team", "attack", "def", "overall", "price", "value"]
    )
    res = dict(zip(['Forward', "Midfielder", "Defender", "Goalkeeper"], positions))

    for key, position in res.items():
        players = position.find_elements(By.TAG_NAME, "tr")
        for player in players:
            player_data = [key]
            table_data = player.find_elements(By.TAG_NAME, "td")
            table_data[0].click()
            player_data = get_player_data(player_data, player.text)

            driver.implicitly_wait(3)
            try:
                # Player value
                player_value = driver.find_element_by_xpath(
                    '//h3[contains(@data-bind,"currency: value, fractionDigits: 1, roundCurrency: '
                    'isSessionPlayer ? RoundCurrency.Downwards : RoundCurrency.Upwards")]'
                )

                # TODO: Get Player nationality as well

                # Close button
                driver.find_element_by_xpath(
                    '//button[contains(@data-bind,"visible: options().showCloseButton")]'
                ).click()
                player_data.append(player_value.text)
            except NoSuchElementException:
                print("Could not find value.")
            finally:
                s = pd.Series(player_data, index=df.columns)
                df = df.append(s, ignore_index=True)

    df.to_csv(f"../data/players_{datetime.datetime.now().strftime('%Y-%m-%d_%H%M')}.csv", index=False)
    df.to_csv(f"../data/players.csv", index=False)

    return 0


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[1]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
