from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import numpy as np
from math import nan
from datetime import datetime

url_UAE = "https://www.investing.com/equities/abu-dhabi"
url_Oman = "https://www.investing.com/equities/oman"
url_Kuwait = "https://www.investing.com/equities/kuwait"
url_Qatar = "https://www.investing.com/equities/qatar"
url_Saudi_Arabia = "https://www.investing.com/equities/saudi-arabia"
url_Bahrain = "https://www.investing.com/equities/bahrain"
s = Service(executable_path="/Users/liaomarova/Desktop/Parsers/chromedriver")
dates = "https://www.investing.com/equities/air-arabia-historical-data"
driver = webdriver.Chrome(service = s)

try:
    format = "%b %d, %Y"
    dates = pd.date_range(start="2021-01-01",end="2021-12-31").to_pydatetime().tolist()[::-1]
    for i in range(len(dates)):
        dates[i] = datetime.strftime(dates[i], format)
    df_ADX = pd.DataFrame(index = dates)
    df_DFM = pd.DataFrame(index = dates)
    df_Bahrain = pd.DataFrame(index = dates)
    df_Qatar = pd.DataFrame(index = dates)
    df_SaudiArabia = pd.DataFrame(index = dates)
    df_Oman = pd.DataFrame(index = dates)
    df_Kuwait = pd.DataFrame(index = dates)



    def parse_data(market, df, file, url):
        
        driver.get(url = url)
        time.sleep(3)
        if(market != 0):
            driver.find_element(By.ID, market).click()
        stocks = [my_elem.get_attribute("href") for my_elem in WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td.bold.left.noWrap.elp.plusIconTd > a")))]
        str1 = "-historical-data"
        str2 = "Historical Data"
        links = []
        for i in stocks:
            sep = i.find('?')
            if(sep != -1):
                links.append(i[:sep] +  str1 + i[sep:])
            else:
                links.append(i + str1)
        for elem in links:
            driver.get(elem)
            print(elem)
            driver.implicitly_wait(5)
            WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.ID, "widgetFieldDateRange"))).click()
            start_date = driver.find_element(By.ID, "startDate")
            end_date = driver.find_element(By.ID, "endDate")
            start_date.clear()
            end_date.clear()
            start_date.send_keys("01/01/2021")
            end_date.send_keys("01/01/2022")
            apply = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.ID, "applyBtn")))
            apply.click()
            
            driver.implicitly_wait(5)
            name_elem = driver.find_element(By.CSS_SELECTOR, "h2.float_lang_base_1.inlineblock")
            name = name_elem.text
            name = name.replace(str2, '')
            mytable = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'table.genTbl.closedTbl.historicalTbl')))
            rows = mytable.find_elements(By.CSS_SELECTOR, 'tr')
            if (len(rows) != 2):
                rows.pop(0)
                arr_date = []
                arr_price = []
                for row in rows:
                    cell = row.find_elements(By.TAG_NAME, 'td')
                    arr_date.append(cell[0].text)
                    arr_price.append(cell[1].text)
                ser = pd.Series(data = arr_price, index = arr_date)
                ser = ser.reindex(df.index, fill_value = nan)
                df[name] = ser
            driver.implicitly_wait(5)
        df.to_csv(file)

    parse_data('all', df_Qatar, '/Users/liaomarova/Desktop/Parsers/data_Qatar.csv', url_Qatar)
    parse_data('all', df_Bahrain, '/Users/liaomarova/Desktop/Parsers/data_Bahrain.csv', url_Bahrain)
    parse_data(941336, df_ADX, '/Users/liaomarova/Desktop/Parsers/data_ADX.csv', url_UAE)
    parse_data(12522, df_DFM, '/Users/liaomarova/Desktop/Parsers/data_DFM.csv', url_UAE)
    parse_data('all', df_SaudiArabia, '/Users/liaomarova/Desktop/Parsers/data_SaudiArabia.csv', url_Saudi_Arabia)
    parse_data('all', df_Oman, '/Users/liaomarova/Desktop/Parsers/data_Oman.csv', url_Oman)
    parse_data(0, df_Kuwait, '/Users/liaomarova/Desktop/Parsers/data_Kuwait.csv', url_Kuwait)
    

except Exception as ex:
    print(ex)
finally:
    print("DONE")
    driver.close()
    driver.quit()
