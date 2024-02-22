#!/bin/python
# -*- coding: utf-8 -*-
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def extract_table_data(rows):
    """
    Extracts data from table rows and columns.
    :param rows: Placeholder.
    :return: DataFrame containing the extracted data.
    """
    data = []
    for row in rows:
        # For each row, find all cells
        cells = row.find_elements(By.TAG_NAME, "td")
        row_data = [cell.text for cell in cells]
        adresse_href = [cell.find_element(By.TAG_NAME, "a").get_attribute('href') for
                        cell in cells[:1] if cell.find_elements(By.TAG_NAME, "a")]
        lage_href = [cell.find_element(By.TAG_NAME, "a").get_attribute('href') for cell
                     in cells[-1:] if cell.find_elements(By.TAG_NAME, "a")]
        data.append(row_data + adresse_href + lage_href)

    return pd.DataFrame(data, columns=["Adresse", "Zimmer", "Eigenmittel",
                                       "Monatliche Kosten", "Lage URL", "Page URL",
                                       "Location URL"])


def main():
    logger = logging.getLogger(__name__)
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    logger.info("Opening Sozialbau AG > Sofort Verfuegbar.")
    driver.get("https://www.sozialbau.at/angebot/sofort-verfuegbar")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "c115"))
    )

    container_element = driver.find_element(By.ID, "c115")
    tbody = container_element.find_element(By.TAG_NAME, "tbody")
    rows = tbody.find_elements(By.TAG_NAME, "tr")

    # Extract data from the table
    df = extract_table_data(rows)

    logger.info("Data extraction complete. Saving to CSV.")
    df.to_csv(
        project_dir / f"data/flats_{datetime.datetime.now().strftime('%Y-%m-%d_%H%M')}.csv",
        index=False,
    )
    df.to_csv(project_dir / "data/flats.csv", index=False)
    driver.close()
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
