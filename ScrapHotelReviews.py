#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 14:04:48 2021

@author: Huygens Ravelomanana
"""

from selenium import  webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (NoSuchElementException,
                                        TimeoutException,
                                        ElementClickInterceptedException,
                                        StaleElementReferenceException)

import time
from  datetime import datetime
#import time
import os
import pandas as pd

chromedriver_location = os.environ["HOME"] + "/chromedriver_linux64/chromedriver"
url = "https://www.google.com/travel/hotels"



############## Defining a general class for the scrapping ####################

class GoogleSearchHotel():
    """"A class for scrapping data from google travel hotel"""
    def __init__(self, chromedriver_location, url):
        self.chromedriver_location = chromedriver_location
        self.url = url
    
    def launch(self):
        # launching the web browser 
        self.driver = webdriver.Chrome(chromedriver_location)
        
        # launching the website
        self.driver.maximize_window()
        self.driver.get(url)
    
    def quit(self):
        # closing the window
        self.driver.quit()
        del self
    
    def switch_window(self, window_index):
        """switching focus to the newly opened window"""
        new_window = self.driver.window_handles[window_index]
        self.driver.switch_to.window(new_window)

    def search(self, key):
        """method for searching using the search bar"""
        #  xpath for the search input
        xpath = '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/div/c-wiz/div[1]/\
            div[1]/div[2]/c-wiz/div/div[1]/div[2]/div[1]/div/div[1]/input'

        # finding the serach input
        search = self.driver.find_element(By.XPATH, xpath)
        
        # doing the search
        search.clear()
        search.send_keys(key)
        search.send_keys(Keys.RETURN)
    
    def set_lowcost(self):
        """Method for selecting only low cost hotels.
        Should be called only after a search has been called"""
        
            
        all_filter_xp = '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/div/c-wiz/\
            div[1]/div[1]/div[3]/div/div[1]/div/div[2]/div/div/div/div[1]/\
                div/button/span'
        
        radio_xp = '/html/body/c-wiz[2]/div/div[2]/div/c-wiz/div[1]/div[1]/\
div[3]/div/div[1]/div/div[2]/div/div/div[2]/div[2]/div[1]/div[2]/\
div/div[1]/div/div/section[2]/div/div/div/div[2]/div/input'
        
        self.driver.find_element(By.XPATH,
                                 all_filter_xp).click()

        # giving time for the element to load
        time.sleep(3)
        
        self.driver.find_element(By.XPATH, radio_xp).click()
    
    def get_elements(self, method, key):
        """Getting a list of elements
        Input:
        ------
                method: By.
                key: string
        """
        
        try:
            myElem = WebDriverWait(self.driver, 100).\
                        until(EC.\
                              presence_of_element_located(
                                    (method,
                                     key)
                                ))

        except TimeoutException:
            print("Loading took too much time!")

        # getting the list of all hotels in the current page
        result = self.driver.find_elements(method, key)
        
        return result

    
    def sort_by_lowest_score(self):
        """Sort the reviews by lowest scrore"""

        other_sites = "Reviews on other travel sites" in self.driver.page_source
        traveler_type = "Ratings by traveler type" in self.driver.page_source
        mention = "People often mention" in self.driver.page_source

        #dropdwn_name = "vRMGwf.rnvjOc" 

        if (other_sites and traveler_type) and mention:
            self.driver.execute_script("window.scrollTo(0, 650);") 
            dropdwn_xp = '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/div[2]/div/\
            div[3]/c-wiz/c-wiz/div/div/div/div[5]/div[3]/span[1]/span/div/\
                div[1]/div[1]/div[1]/span'
            lowest_score_xp = '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/div[2]/\
                div/div[3]/c-wiz/c-wiz/div/div/div/div[5]/div[3]/span[1]/\
                    span/div[1]/div[2]/div[4]/span'

        elif other_sites and traveler_type:
            self.driver.execute_script("window.scrollTo(0, 650);") 
            dropdwn_xp = '//*[@id="reviews"]/c-wiz/c-wiz/div/div/div/\
            div[5]/div[3]/span[1]/span/div/div[1]/div[1]/div[1]/span[1]'
            lowest_score_xp = '//*[@id="reviews"]/c-wiz/c-wiz/div/div/div/\
            div[5]/div[3]/span[1]/span/div[1]/div[2]/div[4]/span'

        elif (other_sites or traveler_type) and mention: 
            self.driver.execute_script("window.scrollTo(0, 400);")
            dropdwn_xp = '//*[@id="reviews"]/c-wiz/c-wiz/div/div/div/\
            div[4]/div[3]/span/span/div/div[1]/div[1]/div[1]/span'
            lowest_score_xp = '//*[@id="reviews"]/c-wiz/c-wiz/div/div/div/\
            div[4]/div[3]/span[1]/span/div[1]/div[2]/div[4]/span'
        elif other_sites or traveler_type: 
            self.driver.execute_script("window.scrollTo(0, 400);")
            dropdwn_xp = '//*[@id="reviews"]/c-wiz/c-wiz/div/div/div/\
            div[4]/div[2]/span[1]/span/div/div[1]/div[1]/div[1]/span'
            lowest_score_xp = '//*[@id="reviews"]/c-wiz/c-wiz/div/div/\
            div/div[4]/div[2]/span[1]/span/div[1]/div[2]/div[4]/span'

        else:
            dropdwn_xp = '//*[@id="reviews"]/c-wiz/c-wiz/div/div/div/\
            div[3]/div[2]/span/span/div/div[1]/div[1]/div[1]/span'
            lowest_score_xp = '//*[@id="reviews"]/c-wiz/c-wiz/div/div/div/\
            div[3]/div[2]/span/span/div[1]/div[2]/div[4]/span'


        try:   
            WebDriverWait(self.driver,10).until(EC.element_to_be_clickable(
                (By.XPATH,dropdwn_xp))).click()
            WebDriverWait(self.driver,10).until(EC.element_to_be_clickable(
                (By.XPATH,lowest_score_xp))).click()
        except  TimeoutException:
            pass
        except ElementClickInterceptedException:
            try:
                self.driver.execute_script("window.scrollBy(0,60);")
                WebDriverWait(self.driver,10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH,lowest_score_xp))).click()
            except:
                pass


    def get_reviews(self, sort_by_lowest=False):
        # initializing a review list
        review_list = []

        click_next = True

        while click_next:
            # giving time for the page to load completely
            time.sleep(4)
            
            hotels_sublist = self.get_elements(By.CLASS_NAME,
                                               "spNMC.nlwZxb.lRagtb")

            for hotel_link in hotels_sublist:
                #  getting hotel's name
                hotel_name = hotel_link.accessible_name.split(', ')[1]

                # clicking on the search
                actions = ActionChains(self.driver)

                actions.click(hotel_link).perform()
        
                # switching focus to the newly opened window
                try:
                    self.switch_window(1)
                except IndexError:
                    print("\nIndexError: \tExiting the loop\n")
                    break

                # giving time for the page to load completely 
                time.sleep(4)
                self.driver.execute_script("window.scrollTo(0,0);")
                time.sleep(3)

                # sorting the lowest score
                if sort_by_lowest:
                    self.sort_by_lowest_score()

                # giving time for the page to load completely
                time.sleep(4)
                try:
                    WebDriverWait(self.driver, 100).until(
                        EC.presence_of_element_located((By.CLASS_NAME,
                                                        "K7oBsc")))                                            
                except TimeoutException:
                    print("Loading took too much time!")

                # scrolling up to the bottom of the page
                self.driver.execute_script(
                    "window.scrollTo(0,document.body.scrollHeight)")
                # getting all review blocks/rows in the current page
                all_reviews = self.get_elements(By.CLASS_NAME, "Svr5cf.bKhjM")

                # getting each single review
                for each in all_reviews:
                    # getting numerical rating
                    try:
                        rating = each.find_element(By.CLASS_NAME,
                                                   "MfbzKb").text
                    except StaleElementReferenceException:
                        break

                    # getting text review
                    review_div = each.find_element(By.CLASS_NAME, "K7oBsc")
                    # setting default review as empty string
                    review = ""

                    try:
                        review = review_div.find_element(By.TAG_NAME,
                                                         "span").text
                    except NoSuchElementException:
                        pass

                    # appending the result as a dictionary
                    result = {"hotel_name": hotel_name,
                              "review": review,
                              "rating": rating}
                    review_list.append(result)

                # close current tab
                self.driver.close()

                # switching back to main window
                self.switch_window(0)

            # storing the next and previous text for next and previous button
            next_previous = self.get_elements(By.CSS_SELECTOR,
                                              ".RveJvd.snByac")


            # getting to the next button and clicking it
            # we need to consider the first page separately since the xpath
            # of the next button in the first page and the other page are different
            if "Next" in map(lambda x: x.text, next_previous):
                if "Previous"  not in map(lambda x: x.text, next_previous):
                    next_link =  self.driver.find_element(By.XPATH,
                       '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/div/c-wiz/\
                       div[1]/div[2]/div[1]/div/main/div/c-wiz/div[1]/\
                           div[8]/div/div')
                    actions.click(next_link).perform()
                else:
                    next_link =  self.driver.find_element(By.XPATH,
                       '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/div/c-wiz/\
                           div[1]/div[2]/div[1]/div/main/div/c-wiz/div[1]/\
                               div[8]/div[2]/div')
                    actions.click(next_link).perform()

            # breaking out of the loop if we are at the last page
            else:
                click_next = False
                print("\nFinished\n")
                break;
        
        return pd.DataFrame(review_list)

##############################################################################

########### Defining a scrapping function ####################################

def scrap_reviews(location,
                  lowcost=False,
                  sort_by_lowest=False,
                  dir_path = f"revies.{datetime.now()}"):

    """Scrapping google hotel reviews for the input location
       `location`
       Input:
       -----
       
       Output:
       ------
               pandas.Dataframe
    """

    SearchInstance = GoogleSearchHotel(chromedriver_location, url)
    SearchInstance.launch()
    SearchInstance.search(location)
    
    if lowcost:
        SearchInstance.set_lowcost()
    
    review_df = SearchInstance.get_reviews(sort_by_lowest=sort_by_lowest)
    
    # saving the search result to local directory
    review_df.to_csv(dir_path)
    
    # closing the browser window
    SearchInstance.quit()
    
    # return the data if needed for further processing
    return review_df

##############################################################################

if __name__ == "__main__":
    
    scrap_reviews("Madagascar",
                  dir_path='data/raw_review_data.csv')
    
    # getting more negative reviews data
    arg_list = [
                ("Madagascar", "low_price_data_mg.csv"),
                ("Hong Kong", "low_price_data_HK.csv"),
                ("Hanoi", "low_price_data_Hanoi.csv"),
                ("Kuala Lumpur", "low_price_data_kl.csv"),
                ("Macao", "low_price_data_Macao.csv"),
                ]
    
    
    for location, filename in arg_list:
        scrap_reviews(location,
                      lowcost=True,
                      sort_by_lowest=True,
                      dir_path="data/"+filename)
    

    
