import sys, time, glob, pickle, os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from tensorflow.keras.models import load_model
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")  # 브라우저 보려면 여기까지 주석
options.add_argument('lang=ko_KR')
options.add_argument('disable_gpu')

driver = webdriver.Chrome('./chromedriver', options=options)

form_window = uic.loadUiType('./earthquake_pred.ui')[0]

class start_crawling(QThread):  # 이미지 변경 및 크롤링 스레드
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent  # 메인에서 지정된 self변수를 스레드에서 사용할 수 있게 parent로 접근
    def run(self):
        row = [-180, -150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150, 180]
        col = [90, 60, 30, 0, -30, -60, -90]
        print(self.parent.btn)
        pm = QPixmap('./gui/anew_split_map/anew_map_{}.gif'.format(self.parent.btn))  # 라벨에 이미지 불러오기
        btn = int(self.parent.btn)

        self.parent.lbl_partmap.show()
        self.parent.lbl_partmap.setPixmap(pm)
        self.parent.lbl_map.hide()
        self.parent.hide_btn(False)
        self.parent.btn_readypred.hide()
        self.parent.btn_startpred.show()

        temp_x = (btn % 12) if btn % 12 != 0 else 12
        temp_y = (btn // 12) if temp_x == 12 else (btn // 12) + 1
        self.parent.loc_up = col[temp_y - 1]
        self.parent.loc_left = row[temp_x - 1]
        loc = 'X_{}~{},Y_{}~{}'.format(self.parent.loc_left, self.parent.loc_left + 30, self.parent.loc_up - 30, self.parent.loc_up)
        self.parent.status_num = 2
        self.parent.model_loc = ''
        for i in self.parent.model_data:
            if loc in i:
                self.parent.model_loc = i
                if self.parent.crawling_recent_data(self.parent.loc_up, self.parent.loc_up - 30, self.parent.loc_left, self.parent.loc_left + 30):
                    self.parent.lbl_result.setText(loc + ' 위치의 모델과 자료를 찾았습니다.')
                else:
                    self.parent.lbl_result.setText(loc + ' 위치의 모델은 존재하지만 충분한 최근 데이터가 부족합니다.')
                    self.parent.btn_startpred.hide()
                break
        if self.parent.model_loc == '':
            self.parent.lbl_result.setText(loc + ' 위치의 표본이 부족하여 모델이 존재하지 않습니다.')
            self.parent.btn_startpred.hide()
        print('check')
        self.parent.status_num = 6
        self.parent.lbl_load.hide()
        self.parent.activate_butten(True)

class run_status(QThread):  # 상태 표시줄 스레드
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.working = True
        self.status_str = ''
    def run(self):
        while self.working:
            if self.parent.status_num == 0: self.status_str = 'Ready'
            elif self.parent.status_num == 1: self.status_str = 'Location input ready'
            elif self.parent.status_num == 2: self.status_str = 'Searching for model and location'
            elif self.parent.status_num == 3: self.status_str = 'Preprocessing'
            elif self.parent.status_num == 4: self.status_str = 'Model run'
            elif self.parent.status_num == 5: self.status_str = 'Prediction done'
            elif self.parent.status_num == 6: self.status_str = 'Crawling and model search completed'
            if self.parent.status_num in [2, 4]: self.status_str = self.status_str + '..' * self.parent.time_counter
            self.parent.lbl_status.setText(self.status_str)
    def stop(self):  # stop을 사용하려면 스레드에 이 함수를 추가한다.
        self.working = False
        self.quit()
        self.wait(5)

class five_time_count(QThread):  # 시간 스레드, 0 1 2 3 4만 표시된다.
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.working = True
    def run(self):
        while self.working:
            self.parent.time_counter += 1
            if self.parent.time_counter == 5: self.parent.time_counter = 0
            time.sleep(0.5)

    def stop(self):
        self.working = False
        self.quit()
        self.wait(5)

class start_model(QThread):  # 전처리 및 모델 예측 스레드
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
    def run(self):
        self.parent.lbl_result.setText('예측을 시작합니다.')
        self.parent.status_num = 3
        self.parent.btn_startpred.hide()
        recent_data = glob.glob('C:Users/ing02/Downloads/*.csv')
        df = pd.read_csv(recent_data[-1])
        df = df[['time', 'latitude', 'longitude', 'depth', 'mag', 'gap', 'rms']]
        df['depth'].fillna(df['depth'].mean(), inplace=True)
        df['gap'].fillna(500, inplace=True)
        df['rms'].fillna(0, inplace=True)
        df['time'] = pd.to_datetime(df['time'])
        df.sort_values(by='time', ascending=True, inplace=True)
        df.set_index('time', inplace=True)
        df = df[(self.parent.loc_up - 30 <= df['latitude']) & (df['latitude'] <= self.parent.loc_up) & (self.parent.loc_left <= df['longitude']) & (df['longitude'] <= self.parent.loc_left + 30)]
        df.info()
        df = df[-100:]
        scaled_data = self.parent.scaler.transform(df)
        scaled_data = np.array(scaled_data)
        self.parent.model_class(scaled_data)

class Exam(QMainWindow, form_window):
    def __init__(self): # 버튼 누르는 함수 처리해 주는 곳
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Earthquake_prediction_2.3_ver')  # 타이틀 지정
        self.btn_split_map_list = [self.btn_01, self.btn_02, self.btn_03, self.btn_04, self.btn_05, self.btn_06, self.btn_07, self.btn_08, self.btn_09, self.btn_10,
                              self.btn_11, self.btn_12, self.btn_13, self.btn_14, self.btn_15, self.btn_16, self.btn_17, self.btn_18, self.btn_19, self.btn_20,
                              self.btn_21, self.btn_22, self.btn_23, self.btn_24, self.btn_25, self.btn_26, self.btn_27, self.btn_28, self.btn_29, self.btn_30,
                              self.btn_31, self.btn_32, self.btn_33, self.btn_34, self.btn_35, self.btn_36, self.btn_37, self.btn_38, self.btn_39, self.btn_40,
                              self.btn_41, self.btn_42, self.btn_43, self.btn_44, self.btn_45, self.btn_46, self.btn_47, self.btn_48, self.btn_49, self.btn_50,
                              self.btn_51, self.btn_52, self.btn_53, self.btn_54, self.btn_55, self.btn_56, self.btn_57, self.btn_58, self.btn_59, self.btn_60,
                              self.btn_61, self.btn_62, self.btn_63, self.btn_64, self.btn_65, self.btn_66, self.btn_67, self.btn_68, self.btn_69, self.btn_70,
                              self.btn_71, self.btn_72]
        self.model_data = glob.glob('./models/*.h5')
        with open('./datasets/earthquake_minmaxscaler.pickle', 'rb') as f:
            self.scaler = pickle.load(f)
        self.btn_readypred.clicked.connect(self.ready_pred)
        self.btn_startpred.clicked.connect(self.preprocessing)
        self.btn_back.clicked.connect(self.go_home)
        for i in self.btn_split_map_list:
            i.clicked.connect(self.map_location_pick)
        self.go_home()
        self.setFixedSize(817, 629)  # 창 크기 고정
        self.model_loc = ''
        self.loc_up = 0
        self.loc_left = 0
        self.time_counter = 0
        self.Five_time_count = five_time_count(self)
        self.Five_time_count.start()  # 스레드 시작
        self.Run_status = run_status(self)
        self.Run_status.start()

    def go_home(self):  # 메인으로 돌아갈때
        self.lbl_result.setText('Earthquake_prediction_2.3_ver')
        self.status_num = 0
        self.hide_btn(False)
        self.btn_back.hide()
        self.btn_readypred.show()
        self.btn_startpred.hide()
        self.lbl_reddot.hide()
        self.lbl_map.show()
        self.lbl_partmap.hide()
        self.lbl_load.hide()
        [os.remove(f) for f in glob.glob('C:Users/ing02/Downloads/*.csv')]  # 해당 위치의 csv파일을 전부 삭제한다.

    def ready_pred(self):  # 위치 지정
        self.lbl_result.setText('예측 위치를 정해주세요')
        self.status_num = 1
        self.hide_btn(True)
        self.btn_back.show()

    def map_location_pick(self):  # 위치를 정했을때
        self.activate_butten(False)
        self.lbl_result.setText('모델 검색중..')
        self.load_logo('Bean_Eater')
        self.btn = (((self.sender()).objectName()).split('_'))[1]  # 눌린 버튼이 뭔지 확인
        Start_crawling = start_crawling(self)
        Start_crawling.start()


    def crawling_recent_data(self, up, down, left, right):  # 크롤링 코드
        count_xpath = '/html/body/usgs-root/div/usgs-list/cdk-virtual-scroll-viewport/div[1]/usgs-search-results/div/span'
        ed_time = datetime.now()
        e_t = ed_time.strftime('%Y-%m-%d')  # 현재 시각을 문자열로 해당 포맷에 맞게 표시
        de = 60
        t = 4
        self.lbl_result.setText('크롤러가 자료를 수집하고 있습니다.')
        try:
            while True:
                st_time = (ed_time + timedelta(days=-de)).strftime('%Y-%m-%d')  # 시작시간 지정
                url = 'https://earthquake.usgs.gov/earthquakes/map/?extent=12.89749,-175.78125&extent=68.56038,-35.15625&range=search&map=false&search=%7B%22name%22:%22Search%20Results%22,%22params%22:%7B%22starttime%22:%22{}%2000:00:00%22,%22endtime%22:%22{}%2023:59:59%22,%22maxlatitude%22:{},%22minlatitude%22:{},%22maxlongitude%22:{},%22minlongitude%22:{},%22minmagnitude%22:0.5,%22eventtype%22:%22earthquake%22,%22orderby%22:%22time%22%7D%7D'.format(
                    st_time, e_t, up, down, right, left)
                driver.get(url)
                time.sleep(t)
                co = int(((driver.find_element_by_xpath(count_xpath).text).split())[0])
                # 크롤링 여부 판단
                if co >= 150:
                    driver.find_element_by_xpath('/html/body/usgs-root/div/usgs-list/cdk-virtual-scroll-viewport/div[1]/usgs-download-button/div/button').send_keys(Keys.ENTER)
                    time.sleep(0.2)
                    down_url = driver.find_element_by_xpath('//*[@id="mat-dialog-0"]/usgs-download-options/div[1]/ul/li[1]/a').get_attribute('href')
                    driver.get(down_url)
                    time.sleep(0.2)
                    return True
                elif 150 > co >= 100: de += 90
                elif 100 > co >= 40: de += 150
                elif 40 > co >= 10:
                    de += 210
                    t = 6
                else: return False
        except: print('crawling error')
        return False

    def preprocessing(self):  # 전처리 시작
        self.activate_butten(False)
        self.load_logo('Infinity')
        thread_model = start_model(self)
        thread_model.start()

    def model_class(self, scaled_data):  # 모델 예측 및 위치 와 진도 표시
        self.status_num = 4
        scaled_data = scaled_data.reshape(-1, 100, 6)
        model = load_model(self.model_loc)
        print(scaled_data.shape)
        next_eq_pred = model.predict(scaled_data)  # 모델 예측
        next_eq_pred = self.scaler.inverse_transform(next_eq_pred)  # 역 스케일링
        next_eq_pred = (next_eq_pred.tolist())[0]  # 괄호 하나를 벗긴다.
        X = next_eq_pred[1]
        Y = next_eq_pred[0]
        M = next_eq_pred[3]
        qt_cs = round(7 * M, 0)  # 점 크기
        qt_mx = round((310 / 30) * (X - self.loc_left) - qt_cs / 2, 0)  # x좌표 이동 수식
        qt_my = round((401 / 30) * (self.loc_up - Y) - qt_cs / 2, 0)  # y좌표 이동 수식
        self.lbl_result.setText('다음 지진은 위도 {}, 경도 {}, 깊이 {}km 지점에 규모 {}이(가) 예상됩니다.\n(북위 : +, 남위 : -, 서경 : -, 동경 : +)'.format(round(Y, 2), round(X, 2), round(next_eq_pred[2], 2), round(M, 1)))
        self.lbl_reddot.show()
        self.lbl_reddot.move(185 + qt_mx, 20 + qt_my)  # 점 이동
        self.lbl_reddot.setFixedSize(qt_cs, qt_cs)  # 점 크기 지정
        [os.remove(f) for f in glob.glob('C:Users/ing02/Downloads/*.csv')]
        self.status_num = 5
        self.lbl_load.hide()
        self.activate_butten(True)

    def activate_butten(self, switch):  # 버튼 활성화 / 비활성화
        for i in [self.btn_back, self.btn_readypred, self.btn_startpred]:
            i.setEnabled(switch)

    def closeEvent(self, QCloseEvent):  # 종료 이벤트
        ans = QMessageBox.question(self, '종료', '종료할까요?', QMessageBox.No | QMessageBox.Yes, QMessageBox.Yes)
        if ans == QMessageBox.Yes:
            driver.close()
            self.Run_status.stop()  # 스레트 정지
            self.Five_time_count.stop()
            [os.remove(f) for f in glob.glob('C:Users/ing02/Downloads/*.csv')]
            QCloseEvent.accept()
        else: QCloseEvent.ignore()

    def load_logo(self, name):  # 로딩 gif 파일 선택 후 실행
        self.movie = QMovie('./gui/{}.gif'.format(name), QByteArray(), self)
        self.movie.setCacheMode(QMovie.CacheAll)
        self.lbl_load.setMovie(self.movie)
        self.movie.start()
        self.lbl_load.show()

    def hide_btn(self, flag):  # 지도 버튼 숨기기
        for i in self.btn_split_map_list:
            if flag: i.show()
            else: i.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())