import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic # ui를 클래스로 바꿔준다.
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

form_window = uic.loadUiType('./earthquake_pred.ui')[0]
form_loading = uic.loadUiType('./loading.ui')[0]

class Exam(QMainWindow, form_window):
    def __init__(self): # 버튼 누르는 함수 처리해 주는 곳
        super().__init__()
        self.setupUi(self)
        # self.lbl_map.show()
        self.btn_startpred.clicked.connect(self.loading)

    def loading(self):
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
        ph = self.parent().geometry().height()
        pw = self.parent().geometry().width()
        self.move(int(pw / 2 - size.width() / 2), int(ph / 2 - size.height() / 2))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())