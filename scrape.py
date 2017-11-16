import re, time
import selenium.common.exceptions as excp
from selenium import webdriver


def split_str(string, pattern):
    new_string = re.split('' + str(pattern) + '', string)
    return new_string


def elem_parse(block):
    result_info = {}
    job_title = block.find_element_by_tag_name("h2")
    result_info['Job Title'] = job_title.text
    result_info['Job URL'] = job_url = job_title.find_element_by_tag_name('a').get_attribute('href')
    company = block.find_element_by_class_name('company')
    result_info['Company'] = company.text
    try:
        result_info['Company URL'] = link = company.find_element_by_tag_name('a').get_attribute('href')
    except excp.NoSuchElementException:
        result_info['Company URL'] = link = "N/a"
    location = block.find_element_by_class_name('location').text
    location = split_str(location, ", ")
    result_info['City'] = location[0]
    result_info['State'] = location[1]
    descr_table = block.find_element_by_class_name('snip')
    try:
        result_info['Salary'] = salary = descr_table.find_element_by_tag_name('nobr').text
    except excp.NoSuchElementException:
        result_info['Salary'] = salary = "N/a"
    result_info['Job Description'] = description = descr_table.find_element_by_tag_name('div').text

    return result_info


def parse(link, proxy=0):
    if proxy != 0:
        profile = webdriver.FirefoxProfile()
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.socks", proxy[0])
        profile.set_preference("network.proxy.socks_port", proxy[1])
        profile.set_preference("network.proxy.socks_version", proxy[2])
        profile.update_preferences()

        driver = webdriver.Firefox(firefox_profile=profile)
    else:
        driver = webdriver.Firefox()

    driver.get(link)
    table = driver.find_element_by_id('resultsCol')

    jobs = []

    try:
        for div in table.find_elements_by_xpath("//div[@class='  row  result']"):
            jobs.append(elem_parse(div))
    except excp.NoSuchElementException:
        pass
    try:
        jobs.append(elem_parse(table.find_element_by_xpath("//div[@class='lastRow  row  result']")))
    except excp.NoSuchElementException:
        pass

    time.sleep(2)
    driver.quit()
    return jobs