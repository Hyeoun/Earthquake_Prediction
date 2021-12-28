import sys
import time

from PyQt5.QtWidgets import *
from PyQt5 import uic # ui를 클래스로 바꿔준다.
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import glob

form_window = uic.loadUiType('./earthquake_pred.ui')[0]
form_loading = uic.loadUiType('./loading.ui')[0]

class Exam(QMainWindow, form_window):
    def __init__(self): # 버튼 누르는 함수 처리해 주는 곳
        super().__init__()
        self.setupUi(self)
        self.btn_split_map_list = [self.btn_01, self.btn_02, self.btn_03, self.btn_04, self.btn_05, self.btn_06, self.btn_07, self.btn_08, self.btn_09, self.btn_10,
                              self.btn_11, self.btn_12, self.btn_13, self.btn_14, self.btn_15, self.btn_16, self.btn_17, self.btn_18, self.btn_19, self.btn_20,
                              self.btn_21, self.btn_22, self.btn_23, self.btn_24, self.btn_25, self.btn_26, self.btn_27, self.btn_28, self.btn_29, self.btn_30,
                              self.btn_31, self.btn_32, self.btn_33, self.btn_34, self.btn_35, self.btn_36, self.btn_37, self.btn_38, self.btn_39, self.btn_40,
                              self.btn_41, self.btn_42, self.btn_43, self.btn_44, self.btn_45, self.btn_46, self.btn_47, self.btn_48, self.btn_49, self.btn_50,
                              self.btn_51, self.btn_52, self.btn_53, self.btn_54, self.btn_55, self.btn_56, self.btn_57, self.btn_58, self.btn_59, self.btn_60,
                              self.btn_61, self.btn_62, self.btn_63, self.btn_64, self.btn_65, self.btn_66, self.btn_67, self.btn_68, self.btn_69, self.btn_70,
                              self.btn_71, self.btn_72]
        self.btn_readypred.clicked.connect(self.ready_pred)
        self.btn_startpred.clicked.connect(self.start_pred)
        self.btn_back.clicked.connect(self.go_home)
        for i in self.btn_split_map_list:
            i.clicked.connect(self.map_location_pick)
        self.hide_btn()
        self.btn_back.hide()
        self.btn_startpred.hide()
        self.setFixedSize(817, 629)

    def go_home(self):
        pm = QPixmap('./gui/map_small.png')
        self.lbl_map.setPixmap(pm)
        self.hide_btn()
        self.btn_back.hide()
        self.btn_readypred.show()
        self.btn_startpred.hide()

    def ready_pred(self):
        for i in self.btn_split_map_list:
            i.show()
        self.btn_back.show()


    def start_pred(self):
        print('start')

    def map_location_pick(self):
        btn = ((self.sender()).objectName()).split('_')
        pm = QPixmap('./gui/split_map/map_{}.gif'.format(btn[1]))
        self.lbl_map.setPixmap(pm)
        self.hide_btn()
        self.btn_readypred.hide()
        self.btn_startpred.show()

    def hide_btn(self):
        for i in self.btn_split_map_list:
            i.hide()

    def Loading(self):
        # 로딩중일때 다시 클릭하는 경우
        try:
            self.loading
            self.loading.deleteLater()

        # 처음 클릭하는 경우
        except:
            self.loading = loading(self)

# Loading Img
class loading(QWidget, form_loading):

    def __init__(self, parent):
        super(loading, self).__init__(parent)
        self.setupUi(self)
        self.center()
        self.show()

        # 동적 이미지 추가
        self.movie = QMovie('./gui/Infinity.gif', QByteArray(), self)
        self.movie.setCacheMode(QMovie.CacheAll)
        # QLabel에 동적 이미지 삽입
        self.lbl_load.setMovie(self.movie)
        self.movie.start()
        # 윈도우 해더 숨기기
        self.setWindowFlags(Qt.FramelessWindowHint)

    # 위젯 정중앙 위치
    def center(self):
        size = self.size()
        ph = 629
        pw = 817
        self.move(int(pw - size.width() - 20), int(ph - size.height() - 23))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())