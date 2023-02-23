# YouTube-Scrapper

## This is YouTube Scrapper Assignment by Utkarsh Gaikwad

# WebApp Homepage Screenshot

![Homepage for my webapp](./UI%20Screenshots/HomePage.jpg)

# URL Scrapped in this example 

[https://www.youtube.com/@PW-Foundation/videos](https://www.youtube.com/@PW-Foundation/videos)

# Steps my YouTube Scrapper will take to get data through Selenium Automatically

1. Selenium will automatically Open the given URL Channel in Chrome browser and maximize window
2. Selenium will scrap all video titles and take top 5 titles
3. Selenium will scroll down and search for thumbnail URL's and get thumbnail URL's
4. Selenium will select first video and click the link
5. Once Inside the video page Selenium will get current url
6. Now Selenium will scroll down and click show more button to get views and dates data
7. Selenium will now go back to channel page and select 2nd video , this process from 4-7 repeats for 5 videos
8. Saves all the data into dictionary
9. Closes the Driver
10. Converts dictionary to pandas DataFrame
11. Saves the dataframe as YTdata.csv file
12. Shows the dataframe on /ytdata page

# Results of Webscrape

![Results of PW Fonudations Channel Webscrape](./UI%20Screenshots/Results.jpg)

# Screenshot of CSV file saved

![Screenshot of CSV file](./UI%20Screenshots/CSVScreenshot.jpg)

# Link to csv file

[Link to generated CSV file](YTdata.csv)

# Link to assignment given

[Link to Assignment given](./Assignment/22%20Feb_Assignment.pdf)