from qfluentwidgets import SplitFluentWindow, FluentIcon, SplashScreen, setTheme, Theme
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize, QTimer
import sys
from main import MyWindow


class Demo(SplitFluentWindow):

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(r'.\resources\melina.png'))
        self.setWindowTitle('基于改进YOLOv8的交通标志检测系统')
        self.splash = SplashScreen(self.windowIcon(), self)
        self.splash.setIconSize(QSize(400, 400))
        self.myWindow = MyWindow()
        self.addSubInterface(self.myWindow, FluentIcon.HOME, '主界面')
        self.navigationInterface.addItem(
            'settingInterface', FluentIcon.SETTING, '设置', onClick=self.myWindow.settingPred)
        self.navigationInterface.addItem(
            'chooseImage', FluentIcon.PHOTO, '选择图像', onClick=self.myWindow.openImage)
        self.navigationInterface.addItem(
            'chooseVideo', FluentIcon.VIDEO, '选择视频', onClick=self.myWindow.openVideo)
        self.navigationInterface.addItem(
            'chooseCam', FluentIcon.CAMERA, '选择摄像头', onClick=self.myWindow.openCam)
        self.navigationInterface.addItem(
            'zoomInterface', FluentIcon.ZOOM_IN, '放大', onClick=self.myWindow.zoomPred)
        self.navigationInterface.addItem(
            'saveImage', FluentIcon.MOVIE, '保存图像', self.myWindow.saveImageOrVideo)
        self.navigationInterface.addItem(
            'saveTxt', FluentIcon.DOCUMENT, '保存txt', self.myWindow.saveTxt)
        self.myWindow.setSomeUi()
        self.updateFrameless()
        self.resize(1200, 800)
        self.move(50, 50)
        self.timer = QTimer()
        self.timer.timeout.connect(self.close_splash)
        self.timer.start(2000)

    def close_splash(self):
        self.splash.finish()


if __name__ == "__main__":
    app = QApplication([])
    window = Demo()
    window.show()
    sys.exit(app.exec_())
