from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_argument('window-size=1920x1080')
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")  # 브라우저 보려면 여기까지 주석
options.add_argument('lang=ko_KR')
options.add_argument('disable_gpu')

driver = webdriver.Chrome('./chromedriver', options=options)

start_m = ['1957-07-01', '1957-10-01', '1956-07-01', '1956-10-01', '1954-07-01', '1954-10-01', '1951-01-01', '1951-04-01', '1951-07-01', '1951-10-01',
           '1943-07-01', '1943-10-01', '1941-01-01', '1941-04-01', '1941-07-01', '1941-10-01', '1937-07-01', '1937-10-01', '1935-07-01', '1935-10-01',
           '1934-07-01', '1934-10-01', '1932-07-01', '1932-10-01', '1931-01-01', '1931-04-01', '1930-01-01', '1930-04-01', '1930-07-01', '1930-10-01']
end_m = ['1957-09-30', '1957-12-31', '1956-09-30', '1956-12-31', '1954-09-30', '1954-12-31', '1951-03-31', '1951-06-30', '1951-09-30', '1951-12-31',
         '1943-09-30', '1943-12-31', '1941-03-31', '1941-06-30', '1941-09-30', '1941-12-31', '1937-09-30', '1937-12-31', '1935-09-30', '1935-12-31',
         '1934-09-30', '1934-12-31', '1932-09-30', '1932-12-31', '1931-03-31', '1931-06-30', '1930-03-31', '1930-06-30', '1930-09-30', '1930-12-31']
for i in range(len(start_m)):
    url = 'https://earthquake.usgs.gov/earthquakes/map/?extent=-89.29634,-270&extent=89.29634,630&range=search&settings=true&search=%7B%22name%22:%22Search%20Results%22,%22params%22:%7B%22starttime%22:%22{}-01%2000:00:00%22,%22endtime%22:%22{}%2023:59:59%22,%22minmagnitude%22:0.5,%22eventtype%22:%22earthquake%22,%22orderby%22:%22time%22%7D%7D'.format(start_m[i], end_m[i])
    try:
        driver.get(url)
        time.sleep(10)
        driver.find_element_by_xpath('/html/body/usgs-root/div/usgs-list/cdk-virtual-scroll-viewport/div[1]/usgs-download-button/div/button').send_keys(Keys.ENTER)
        time.sleep(0.5)
        down_url = driver.find_element_by_xpath('//*[@id="mat-dialog-0"]/usgs-download-options/div[1]/ul/li[1]/a').get_attribute('href')
        driver.get(down_url)
        time.sleep(0.5)
    except:
        print('{} ~ {} 까지의 csv파일 다운에 실패하였습니다.'.format(start_m[i], end_m[i]))

driver.close()