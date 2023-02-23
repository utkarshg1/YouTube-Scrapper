from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service 
import time
import pandas as pd
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import logging


app = Flask(__name__)

import logging
logging.basicConfig(filename='YTWebScrapper.log',level=logging.DEBUG,format= '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    logging.info('Successfully Landed on Home Page')
    return render_template("index.html")

@app.route('/ytdata',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def get_yt_data():
    if request.method == 'POST':
        try:
            url = request.form['content']
            df = selenium_method(url)
            logging.info(f'Succesfull Data Gathered from Youtube Channel :{url}')
            return render_template('result.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)
        except Exception as e:
            logging.info(f'Exception Occured {e}')
            print('Exception Occured :',e)
    else:
        return render_template('index.html')

def selenium_method(url):
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    driver.get(url)
    driver.maximize_window()
    time.sleep(4)
        
    # First Get Titles
    titles = driver.find_elements(By.XPATH,"//yt-formatted-string[@id='video-title']")
    title_text = []
    for i in titles:
        title_text.append(i.text)
    top5titles = title_text[0:5]

    # Get Thumbnails
    driver.execute_script("window.scrollTo(0, 200)")
    time.sleep(2)
    images = driver.find_elements(By.TAG_NAME,'img')
    img_links = []
    for i in images:    
        link = i.get_attribute('src')
        if str(link).find('i.ytimg.com')>0:
            img_links.append(link)
    top5thumbnails = img_links[0:5]

    # Get Video URL, Views and Date
    video_urls = []
    views_exact = []
    dates = []
    for i in range(5):
        driver.get(url)
        time.sleep(2)
        link_finder = driver.find_elements(By.XPATH,"//a[@id='thumbnail']")
        link_finder[i+1].click()
        time.sleep(2)
        video_urls.append(driver.current_url)
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 200)")
        time.sleep(1)
        show_more = driver.find_element(By.XPATH,"//tp-yt-paper-button[@id='expand']")
        show_more.click()
        time.sleep(1)
        views_and_date = driver.find_elements(By.XPATH,"//span[@class='style-scope yt-formatted-string bold']")
        for j in views_and_date:
            text_str = j.text
            if text_str and text_str.strip():
                if text_str.find('views')>0:
                    views_exact.append(text_str)
                else:
                    dates.append(text_str)

    # Creating A final Dictionary
    dct_final = {'title':top5titles,'views':views_exact,'uploadDate':dates,'videoURL':video_urls,'thumbnails':top5thumbnails}
    logging.info('"Loging dict ---> {0}".format(dct_final)')

    # Creating a DataFrame
    df_final = pd.DataFrame(dct_final)

    # Closing driver
    driver.quit()

    # Saving DataFrame
    df_final.to_csv('YTdata.csv')

    logging.info('Data downloaded to YTdata.csv')

    return df_final

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)