from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_argument('window-size=1920x1080')
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")  # 브라우저 보려면 여기까지 주석
options.add_argument('lang=ko_KR')
options.add_argument('disable_gpu')

driver = webdriver.Chrome('./chromedriver', options=options)


months_day = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
months = ['', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
for i in range(2021, 1899, -1):
    if 2021 >= i >= 1991:
        month_gap = 1
    elif 1990 >= i >= 1979:
        month_gap = 3
    else: month_gap = 12
    for j in range(12, 0, -month_gap):
        if j == 2:
            if (i % 4 == 0 and i % 100 != 0 or i % 400 == 0): end_m = '{}-{}-{}'.format(i, j, 29)
            else: end_m = '{}-{}-{}'.format(i, months[j], months_day[j])
        else: end_m = '{}-{}-{}'.format(i, months[j], months_day[j])
        start_m = '{}-{}'.format(i, months[j - (month_gap - 1)])

        url = 'https://earthquake.usgs.gov/earthquakes/map/?extent=-89.29634,-270&extent=89.29634,630&range=search&settings=true&search=%7B%22name%22:%22Search%20Results%22,%22params%22:%7B%22starttime%22:%22{}-01%2000:00:00%22,%22endtime%22:%22{}%2023:59:59%22,%22minmagnitude%22:0.5,%22eventtype%22:%22earthquake%22,%22orderby%22:%22time%22%7D%7D'.format(start_m, end_m)
        try:
            driver.get(url)
            time.sleep(10)
            driver.find_element_by_xpath('/html/body/usgs-root/div/usgs-list/cdk-virtual-scroll-viewport/div[1]/usgs-download-button/div/button').send_keys(Keys.ENTER)
            time.sleep(0.2)
            down_url = driver.find_element_by_xpath('//*[@id="mat-dialog-0"]/usgs-download-options/div[1]/ul/li[1]/a').get_attribute('href')
            driver.get(down_url)
            time.sleep(0.2)
        except:
            print('{}-01 ~ {} 까지의 csv파일 다운에 실패하였습니다.'.format(start_m, end_m))

driver.close()