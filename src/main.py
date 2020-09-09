#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import os


def main():
    logger = logging.getLogger(__name__)
    driver = webdriver.Chrome()
    # Accept terms and conditions
    driver.get("https://en.onlinesoccermanager.com/Login?nextUrl=%2FCareer")
    driver.implicitly_wait(10)
    driver.find_element_by_class_name('custom-checkbox').click()
    driver.find_element_by_class_name('btn-new').click()

    # Login
    driver.implicitly_wait(10)
    driver.find_element_by_id("login-link").click()
    driver.implicitly_wait(10)
    try:
        driver.find_element_by_id("manager-name").send_keys(os.environ['manager-name'])
        driver.find_element_by_id("password").send_keys(os.environ['password'])
    except KeyError:
        logger.info("Please put manager-name and password in .env file.")
    driver.find_element_by_id("login").click()

    # Choose team
    driver.implicitly_wait(10)
    driver.find_element_by_xpath("//h2[text()='Team Analyst']").click()

    # Go to Transerlist
    driver.implicitly_wait(10)
    driver.get("https://en.onlinesoccermanager.com/Transferlist")
    driver.implicitly_wait(10)
    transferlist = driver.find_element_by_id('transfer-list')
    positions = transferlist.find_elements(By.TAG_NAME, "tbody")

    for position in positions:
        players = position.find_elements(By.TAG_NAME, "tr")
        for player in players:
            # Save name, age, club, att, def, ovr, price
            print(player.text)
            # Get id="modal-dialog-buyforeignplayer"
                # Save nationality, value

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
