#!/usr/bin/env python3
import requests
import logging
import argparse
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep


def wait_for_success(condition, times=30, interval=0.2, **kwargs):
    for i in range(times):
        sleep(interval)
        if eval(condition):
            return
    raise ValueError(condition)


def clock_in(username, password, profile_directory):
    options = webdriver.ChromeOptions()
    options.add_argument(f'user-data-dir={profile_directory}')

    for _ in range(10):
        try:
            driver = webdriver.Chrome(
                executable_path=ChromeDriverManager().install(),
                options=options)
            break
        except requests.exceptions.ProxyError:
            logging.info('Retrying')
            sleep(0.2)
    else:
        raise ValueError('Driver installation error')

    try:
        driver.get('http://erp.jd.com/')

        wait_for_success("kwargs['driver'].title == 'ERP登录'", driver=driver)
        sleep(1.0)

        assert len(driver.find_elements_by_id('username')) == 1
        assert len(driver.find_elements_by_id('password')) == 1
        assert len(driver.find_elements_by_tag_name('form')) == 1

        driver.find_element_by_id('username').send_keys(username)
        driver.find_element_by_id('password').send_keys(password)
        driver.find_element_by_tag_name('form').submit()

        wait_for_success("kwargs['driver'].title == '京东企业门户'", driver=driver)
        sleep(1.0)

        assert len(driver.find_elements_by_id('clockLink')) == 1
        driver.find_element_by_id('clockLink').click()

        wait_for_success(
            "'打卡成功' in kwargs['driver'].find_element_by_tag_name('body').get_attribute('innerText')",
            driver=driver)

        sleep(3.0)

        driver.close()

    except Exception as e:
        sleep(30)
        driver.close()
        raise e


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info('Begin')

    parser = argparse.ArgumentParser()
    parser.add_argument('--username', type=str, required=True)
    parser.add_argument('--password', type=str, required=True)
    args = parser.parse_args()

    profile_directory = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'profile')

    for _ in range(20):
        try:
            clock_in(args.username, args.password, profile_directory)
            logging.info('Success')
            break
        except Exception as e:
            logging.error(e)
            logging.info('Retrying')
            sleep(30)
    else:
        logging.info('Failed')
