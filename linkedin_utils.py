"""Utility functions for linked in scraper."""

# standard library imports
import time

# third party imports
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys



# 1. launch web driver -->> for firmware url
def launch_website(url: str) -> WebDriver:
    """To launch the website and return driver
       object.
    """

    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)  # so that borwser doesn't close
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    return driver


# 2. search job title and location
def search_job(driver: WebDriver, job_title:str, location:str):
    """To search for job title in particular location."""

    # clear the job and location fields
    time.sleep(3)
    clear_job = driver.find_element(By.XPATH, '//*[@id="jobs-search-panel"]/form/section[1]/button')
    clear_button = driver.find_element(By.XPATH, '//*[@id="jobs-search-panel"]/form/section[2]/button')
    clear_button.click()
    clear_job.click()

    # insert job title and location in search fields
    time.sleep(3)
    jobtitle_box = driver.find_element(By.XPATH, '//*[@id="job-search-bar-keywords"]')
    jobtitle_box.send_keys(job_title)
    location_box = driver.find_element(By.XPATH, '//*[@id="job-search-bar-location"]')
    location_box.send_keys(location)
    location_box.send_keys(Keys.ENTER)


def adjust_duration(driver: WebDriver):
    """To adjust date for the week."""

    # to bring down drop down menu for date
    time.sleep(4)
    drop_down = driver.find_element(By.XPATH, '//*[@id="jserp-filters"]/ul/li[1]/div/div/button')
    drop_down.click()

    # choose jobs from last week
    last_week = driver.find_element(By.XPATH, '//*[@id="f_TPR-1"]')
    last_week.click()

    # to enter last week options
    enter_last_week =  driver.find_element(By.XPATH, '//*[@id="jserp-filters"]/ul/li[1]/div/div/div/button')
    enter_last_week.click()


def scroll_infinitely(driver: WebDriver) -> None:
    """To scroll infinitely down the webpage
       till all items have been loaded.
    """

    # get the height of website
    time.sleep(4)
    last_height = driver.execute_script("return document.body.scrollHeight")
    RUN = True

    while RUN:
        # scroll all the way to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")  # get new height of page
        if new_height == last_height:
            RUN = False
        last_height = new_height


def extract_job_info(driver: WebDriver, main_list: list) -> None:
    """To extract the job info and return as list."""

    # extract the container element for each job listing
    job_container_list = driver.find_element(By.CSS_SELECTOR, "#main-content > section.two-pane-serp-page__results-list > ul")
    job_list = job_container_list.find_elements(By.CSS_SELECTOR, "li")

    for job in job_list:
        main_list[0].append(job.find_element(By.CSS_SELECTOR, "div.base-search-card__info > h3").text)  # job title
        main_list[1].append(job.find_element(By.CSS_SELECTOR, "div.base-search-card__info > h4").text)  # company name
        main_list[2].append(job.find_element(By.CSS_SELECTOR, "div.base-search-card__info > div > span").text)  # job location
        main_list[3].append(job.find_element(By.CSS_SELECTOR, "div.base-search-card__info > div > time").get_attribute("datetime"))  # time posted
        main_list[4].append(job.find_element(By.CSS_SELECTOR, "a").get_attribute("href"))  # each job link

    # close the window
    time.sleep(2)
    driver.close()


def create_dataframe(main_list: list) -> pd.DataFrame:
    """To create data frame from the extracted data."""

    general_info_dict = {"job title":main_list[0],
                         "company": main_list[1],
                         "location": main_list[2],
                         "date": main_list[3],
                         "link": main_list[4]}

    df = pd.DataFrame(general_info_dict)
    return df
