from pathlib import Path
import os
from typing import List
from loguru import logger

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

EDGE_DRIVER_PATH = str(
    Path(
        r'C:\Users\amrut\PythonProjects\us-visa-appointment-notifier\edgedriver_win64\msedgedriver.exe'
    ).absolute())


def build_web_url(city: str):
    return f'https://visagrader.com/us-visa-time-slots-availability/india-ind/{city}-P147/b1b2-visa-B1#Interview'


def main(city: str):
    driver = webdriver.Edge(executable_path=EDGE_DRIVER_PATH)

    URL = build_web_url(city)
    driver.get(URL)
    time.sleep(10)

    day_picker_month_list = get_dates_in_months(driver)
    stale_available, available = [], []
    for month in day_picker_month_list:
        logger.debug(
            f'Starting search for the month - {month.find_element(By.CLASS_NAME,"DayPicker-Caption").get_property("textContent")}'
        )
        body = month.find_element(By.CLASS_NAME, 'DayPicker-Body')
        outer_html = BeautifulSoup(body.get_property('outerHTML')).find_all()
        for day in outer_html:
            stale_available.append(
                extract_date_based_on_attrs(day,
                                            'DayPicker-Day--staleAvailable'))
            available.append(
                extract_date_based_on_attrs(day, 'DayPicker-Day--available'))

    available = [_ for _ in available if _ is not None]
    stale_available = [_ for _ in stale_available if _ is not None]
    logger.success(f'Available Dates - {",".join(available)}')
    logger.success(f'Available Stale Dates - {",".join(stale_available)}')

    driver.quit()


def get_dates_in_months(driver):
    interview_availability = driver.find_element(
        By.ID, 'Interview-tab-tabpane-availability')
    day_picker_months = interview_availability.find_element(
        By.CLASS_NAME, 'DayPicker-Months')
    day_picker_month_list = day_picker_months.find_elements(
        By.CLASS_NAME, 'DayPicker-Month')

    return day_picker_month_list


def extract_date_based_on_attrs(day, attr: str) -> str:
    if attr in day.attrs['class']:
        try:
            date = day.attrs['aria-label']
        except Exception:
            pass
        else:
            return date


if __name__ == '__main__':
    main('new-delhi')