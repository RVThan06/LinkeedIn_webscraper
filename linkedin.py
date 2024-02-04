"""Linkedin webscraper with selenium browser automation."""

# standard library imports


# third party imports
import linkedin_utils as utils


def main() -> None:
    """Main program function calls."""

    # # 1. Enter the linkedin webpage url
    webpage_url = "https://my.linkedin.com/jobs/search?keywords=Firmware%20Engineering&location=Malaysia&locationId=&geoId=106808692&f_TPR=r604800&position=1&pageNum=0"
    driver =  utils.launch_website(webpage_url)

    # 2. scroll infinitely
    utils.search_job(driver, "firmware engineer", "penang")

    # 3. update the search result to jobs posted last week
    utils.adjust_duration(driver)

    # 4. scroll the page infinitely till bottom
    utils.scroll_infinitely(driver)

    # 5. Extract job info into a list
    main_list = [[] for _ in range(5)]
    utils.extract_job_info(driver, main_list)

    # 6. save the job info in a dataframe
    data_frame = utils.create_dataframe(main_list)
    print(data_frame.head())


if __name__ == '__main__':
    main()
