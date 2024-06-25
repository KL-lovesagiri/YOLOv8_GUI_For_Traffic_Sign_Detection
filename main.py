from PySide6.QtWidgets import QMainWindow, QApplication, QFileDialog, QStyle, QWidget, QTableWidgetItem
from PySide6.QtCore import QTimer, Qt, Signal, QThread
from PySide6.QtGui import QPixmap, QImage, QIcon
from Ui_untitled import Ui_Form
from Ui_untitled2 import Ui_Form2
from Ui_untitled3 import Ui_Form3
from ultralytics import YOLO
import cv2
import torch
import sys
from qfluentwidgets import InfoBar, InfoBarPosition

class_names = [
    'pl80', 'p6', 'p5', 'pm55', 'pl60', 'ip', 'p11', 'i2r', 'p23', 'pg',
    'il80', 'ph4', 'i4', 'pl70', 'pne', 'ph4.5', 'p12', 'p3', 'pl5', 'w13',
    'i4l', 'pl30', 'p10', 'pn', 'w55', 'p26', 'p13', 'pr40', 'pl20', 'pm30',
    'pl40', 'i2', 'pl120', 'w32', 'ph5', 'il60', 'w57', 'pl100', 'w59',
    'il100', 'p19', 'pm20', 'i5', 'p27', 'pl50'
]


# 将BGR的ndarray图像转为QImage
def bgr2qimage(bgrImage):
    height, width, channels = bgrImage.shape
    if channels != 3:
        print("BGR的ndarray图像的通道数有误，不为3！")
    rgbImage = cv2.cvtColor(bgrImage, cv2.COLOR_BGR2RGB)
    return rgb2qimage(rgbImage, width, height)


# 将RGB的ndarray图像转为QImage
def rgb2qimage(rgbImage, width, height):
    image = QImage(rgbImage.data, width, height, QImage.Format_RGB888)
    image = image.copy()  # 深拷贝，防止原始图像被意外更改
    return image


class MyWindow(QWidget, Ui_Form):
    frameChanged = Signal(int)
    imageChanged = Signal(object)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.model = YOLO(
            r'.\ptfolder\best.pt')
        self.timer = QTimer()  # 计时器
        self.timer.setInterval(10)
        self.timerCam = QTimer()  # 用于摄像头的计时器
        self.timerCam.setInterval(10)
        self.videoCamOnly = None  # 实时检测的VideoCapture类
        self.video = None  # 视频检测的VideoCapture类
        self.isPaused = True  # 是否暂停
        self.totalFrames = 1  # 视频总帧数
        self.currentFrame = 0  # 当前帧数
        self.nowImageSrc = ''  # 当前图片路径（选择图片时使用）
        self.nowImage = None  # 当前图片（选择视频时使用）
        self.nowVideoSrc = ''  # 当前视频路径（选择视频时使用）
        self.iou = 0.7
        self.conf = 0.25
        self.maxdetnum = 300
        self.settingWindow = SettingWindow(self)  # 检测设置子窗口
        self.zoomWindow = ZoomWindow(self)  # 放大目标图像子窗口
        self.bind()
        properties = torch.cuda.get_device_properties(0)
        whetherCudaAvailable = torch.cuda.is_available()
        print(properties.name)
        print(whetherCudaAvailable)
        self.setSomeUi()

    def setSomeUi(self):
        self.resetButton.setIcon(
            self.style().standardPixmap(QStyle.SP_MediaStop))
        self.startButton.setIcon(
            self.style().standardPixmap(QStyle.SP_MediaPlay))
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(
            ['Class', 'X', 'Y', 'W', 'H', 'Confidence'])
        self.setWindowTitle('YOLOV8交通标志检测系统')
        self.setWindowIcon(QIcon(r'.\resources\melina.png'))
        self.settingWindow.setWindowIcon(QIcon(r'.\resources\melina.png'))
        self.zoomWindow.setWindowIcon(QIcon(r'.\resources\melina.png'))
        self.widget.setStyleSheet(
            "border-radius: 50px;background-color: rgba(255, 255, 0, 128);")
        self.widget_2.setStyleSheet(
            "border-radius: 50px;background-color: rgba(0, 255, 0, 128);")
        self.progressBar_2.hide()
        self.progressBar_3.hide()

    def bind(self):
        self.timer.timeout.connect(self.videoPred)
        self.frameChanged.connect(self.updateProgressBar)
        self.resetButton.clicked.connect(self.resetVideo)
        self.startButton.clicked.connect(self.startOrStopPred)
        self.imageChanged.connect(self.zoomWindow.setZoomImage)
        self.timerCam.timeout.connect(self.camPred)

    # 得到缩放后的QPixmap
    def getScaledQPixmap(self, image):
        return QPixmap(image).scaled(500, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

    # 选择图片
    def openImage(self):
        print("开始检测图片！")
        self.timer.stop()
        self.timerCam.stop()
        filePath, _ = QFileDialog.getOpenFileName(
            self, '选择一张图片', r'.\picture', 'Images (*.png *.jpg *.jpeg)')
        if filePath != '':
            self.initializeSomething()
            self.resetButton.hide()
            self.nowImageSrc = filePath
            self.inputLabel.setPixmap(self.getScaledQPixmap(filePath))
            InfoBar.success(
                title='检测',
                content="开始检测图片！",
                orient=Qt.Horizontal,
                isClosable=False,   # disable close button
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )

    # 选择视频
    def openVideo(self):
        print("开始检测视频！")
        self.timer.stop()
        self.timerCam.stop()
        filePath, _ = QFileDialog.getOpenFileName(
            self, '选择一个视频', r'.\video', 'Videos (*.mp4 *.avi *.gif)')
        if filePath != '':
            self.initializeSomething()
            self.video = cv2.VideoCapture(filePath)
            self.nowVideoSrc = filePath
            self.totalFrames = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
            self.videoFirstFrameNoPred()
            InfoBar.success(
                title='检测',
                content="开始检测视频！",
                orient=Qt.Horizontal,
                isClosable=False,   # disable close button
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )

    # 单个图片的检测
    def imagePred(self, filePath):
        results = self.model.predict(
            filePath, iou=self.iou, conf=self.conf, max_det=self.maxdetnum)
        imageNdarray = results[0].plot()
        self.demonstrateResults(results)
        InfoBar.success(
            title='检测',
            content="完成对图片的检测！",
            orient=Qt.Horizontal,
            isClosable=False,   # disable close button
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )
        return bgr2qimage(imageNdarray)

    # 选择视频或回到视频开头后保证左边显示视频的第0帧，右边不显示
    def videoFirstFrameNoPred(self):
        ret, firstImage = self.video.read()  # 读取第0帧的图片
        if ret:
            self.nowImage = firstImage
            firstImage = bgr2qimage(firstImage)
            self.inputLabel.setPixmap(self.getScaledQPixmap(firstImage))
            self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 重置到第0帧

    # 视频预测时定时器每个时间间隔触发的检测
    def videoPred(self):
        ret, tempImage = self.video.read()
        if not ret:
            self.timer.stop()
            self.isPaused = True
            InfoBar.success(
                title='检测',
                content="完成对视频的检测！",
                orient=Qt.Horizontal,
                isClosable=False,   # disable close button
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
        else:
            self.nowImage = tempImage
            results = self.model.predict(
                tempImage, iou=self.iou, conf=self.conf, max_det=self.maxdetnum)
            self.demonstrateResults(results)
            outputImageNdarray = results[0].plot()
            outputImage = bgr2qimage(outputImageNdarray)
            tempImage = bgr2qimage(tempImage)
            self.inputLabel.setPixmap(self.getScaledQPixmap(tempImage))
            self.outputLabel.setPixmap(self.getScaledQPixmap(outputImage))
            self.imageChanged.emit(outputImage)
            self.currentFrame += 1
            self.frameChanged.emit(self.currentFrame)

    # 回到视频开头
    def resetVideo(self):
        if self.video:
            self.timer.stop()
            self.isPaused = True
            self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 重置到第0帧
            self.currentFrame = 0
            self.frameChanged.emit(self.currentFrame)
            self.outputLabel.setPixmap(QPixmap())
            self.imageChanged.emit(QImage())
            self.outputLabel.setText('目标图像')
            self.videoFirstFrameNoPred()
        else:
            InfoBar.error(
                title='错误',
                content="当前不是视频检测任务，不能回退",
                orient=Qt.Horizontal,
                isClosable=False,   # disable close button
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )

    # 根据当前帧数更新进度条
    def updateProgressBar(self, frameNumber):
        self.progressBar.setValue(frameNumber / self.totalFrames * 100)

    # 选择图片或视频时的初始化
    def initializeSomething(self):
        if self.video != None:
            self.video.release()
        if self.videoCamOnly != None:
            self.videoCamOnly.release()
        self.video = None
        self.videoCamOnly = None
        self.isPaused = True  # 是否暂停
        self.totalFrames = 1  # 视频总帧数
        self.currentFrame = 0  # 当前帧数
        self.nowImageSrc = ''  # 当前图片路径（选择图片时使用）
        self.nowImage = None  # 当前图片（选择视频时使用）
        self.nowVideoSrc = ''  # 当前视频路径（选择视频时使用）
        self.frameChanged.emit(self.currentFrame)
        self.inputLabel.setPixmap(QPixmap())
        self.outputLabel.setPixmap(QPixmap())
        self.imageChanged.emit(QImage())
        self.inputLabel.setText('原始图像')
        self.outputLabel.setText('目标图像')
        self.startButton.show()
        self.resetButton.show()
        self.progressBar.show()

    # 点击开始按钮，开始或是停止检测
    def startOrStopPred(self):
        if self.nowImageSrc != '':  # 当前正在检测图片
            outputImage = self.imagePred(self.nowImageSrc)
            self.outputLabel.setPixmap(self.getScaledQPixmap(outputImage))
            self.imageChanged.emit(outputImage)
            self.currentFrame = 1  # 检测完一遍
            self.frameChanged.emit(self.currentFrame)
        elif self.nowVideoSrc != '':  # 当前正在检测视频
            if self.isPaused:  # 已暂停
                self.timer.start()
            else:
                self.timer.stop()
            self.isPaused = not self.isPaused
        elif self.nowImageSrc == '' and self.nowVideoSrc == '' and self.video == None and self.videoCamOnly == None:
            InfoBar.error(
                title='错误',
                content="当前没有检测任务",
                orient=Qt.Horizontal,
                isClosable=False,   # disable close button
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )

    # 展示设置窗口
    def settingPred(self):
        self.settingWindow.move(10, 10)
        self.settingWindow.show()

    # 展示放大窗口
    def zoomPred(self):
        self.zoomWindow.move(100, 100)
        self.zoomWindow.show()

    # 设置引起的重测
    def rePred(self, iou, conf, maxdetnum):
        self.iou = iou
        self.conf = conf
        self.maxdetnum = maxdetnum
        if self.nowImageSrc != '':  # 当前正在检测图片
            if self.currentFrame:  # 点击过startButton，立即重测
                self.startOrStopPred()
        elif self.nowVideoSrc != '':  # 当前正在检测视频
            if self.isPaused and self.currentFrame:  # 已暂停，立即重测
                results = self.model.predict(
                    self.nowImage, iou=self.iou, conf=self.conf, max_det=self.maxdetnum)
                self.demonstrateResults(results)
                outputImageNdarray = results[0].plot()
                outputImage = bgr2qimage(outputImageNdarray)
                self.outputLabel.setPixmap(self.getScaledQPixmap(outputImage))
                self.imageChanged.emit(outputImage)

    # 保存图像
    def saveImageOrVideo(self):
        if self.nowImageSrc == '' and self.nowVideoSrc == '' and self.video == None and self.videoCamOnly == None:
            InfoBar.error(
                title='错误',
                content="当前没有检测任务",
                orient=Qt.Horizontal,
                isClosable=False,   # disable close button
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
        elif self.videoCamOnly != None:
            InfoBar.error(
                title='错误',
                content="摄像头检测不支持保存",
                orient=Qt.Horizontal,
                isClosable=False,   # disable close button
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
        else:
            self.saveThread = SaveThread(self)  # 保存图像线程
            self.saveThread.finished.connect(self.updateSaveImageOrVideo)
            InfoBar.warning(
                title='保存图像',
                content="开始保存标注后的图像文件",
                orient=Qt.Horizontal,
                isClosable=False,   # disable close button
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
            self.progressBar_2.show()
            self.saveThread.start()

    # 保存图像之后显示成功信息
    def updateSaveImageOrVideo(self):
        InfoBar.success(
            title='保存图像',
            content="成功保存标注后的图像文件",
            orient=Qt.Horizontal,
            isClosable=False,   # disable close button
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )
        self.progressBar_2.hide()
        self.saveThread.deleteLater()

    # 保存txt
    def saveTxt(self):
        if self.nowImageSrc == '' and self.nowVideoSrc == '' and self.video == None and self.videoCamOnly == None:
            InfoBar.error(
                title='错误',
                content="当前没有检测任务",
                orient=Qt.Horizontal,
                isClosable=False,   # disable close button
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
        elif self.videoCamOnly != None:
            InfoBar.error(
                title='错误',
                content="摄像头检测不支持保存",
                orient=Qt.Horizontal,
                isClosable=False,   # disable close button
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
        else:
            self.saveTxtThread = SaveTxtThread(self)  # 保存txt线程
            self.saveTxtThread.finished.connect(self.updateSaveTxt)
            InfoBar.warning(
                title='保存txt',
                content="开始保存标注txt文件",
                orient=Qt.Horizontal,
                isClosable=False,   # disable close button
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
            self.progressBar_3.show()
            self.saveTxtThread.start()

    # 保存图像之后显示成功信息
    def updateSaveTxt(self):
        InfoBar.success(
            title='保存txt',
            content="成功保存标注txt文件",
            orient=Qt.Horizontal,
            isClosable=False,   # disable close button
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )
        self.progressBar_3.hide()
        self.saveTxtThread.deleteLater()

    # 得到预测结果后展示在表格中
    def demonstrateResults(self, results):
        self.tableWidget.setRowCount(0)
        for r in results:
            boxes = r.boxes
            cls = boxes.cls.tolist()
            xywh = boxes.xywh.tolist()
            conf = boxes.conf.tolist()
            length = len(cls)
            self.tableWidget.setRowCount(length+1)
            for i, (c_float, (x, y, w, h), conf_val) in enumerate(zip(cls, xywh, conf)):
                c_int = int(c_float)
                now_name = class_names[c_int]
                # 设置单元格内容
                self.tableWidget.setItem(i, 0, QTableWidgetItem(now_name))
                self.tableWidget.setItem(i, 1, QTableWidgetItem(str(x)))
                self.tableWidget.setItem(i, 2, QTableWidgetItem(str(y)))
                self.tableWidget.setItem(i, 3, QTableWidgetItem(str(w)))
                self.tableWidget.setItem(i, 4, QTableWidgetItem(str(h)))
                self.tableWidget.setItem(
                    i, 5, QTableWidgetItem(f"{conf_val:.2f}"))

    # 打开摄像头
    def openCam(self):
        print("开始检测摄像头！")
        self.timer.stop()
        self.timerCam.stop()
        self.initializeSomething()
        self.videoCamOnly = cv2.VideoCapture(0)  # 打开摄像头
        self.timerCam.start()
        self.startButton.hide()
        self.resetButton.hide()
        self.progressBar.hide()
        InfoBar.success(
            title='检测',
            content="开始检测摄像头！",
            orient=Qt.Horizontal,
            isClosable=False,   # disable close button
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )

    # 摄像头预测时定时器每个时间间隔触发的检测
    def camPred(self):
        ret, tempImage = self.videoCamOnly.read()
        if not ret:
            self.timerCam.stop()
            self.isPaused = True
        else:
            self.nowImage = tempImage
            results = self.model.predict(
                tempImage, iou=self.iou, conf=self.conf, max_det=self.maxdetnum)
            self.demonstrateResults(results)
            outputImageNdarray = results[0].plot()
            outputImage = bgr2qimage(outputImageNdarray)
            tempImage = bgr2qimage(tempImage)
            self.inputLabel.setPixmap(self.getScaledQPixmap(tempImage))
            self.outputLabel.setPixmap(self.getScaledQPixmap(outputImage))
            self.imageChanged.emit(outputImage)


class SaveThread(QThread):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.nowImageSrc = self.parent.nowImageSrc
        self.nowVideoSrc = self.parent.nowVideoSrc
        self.iou = self.parent.iou
        self.conf = self.parent.conf
        self.maxdetnum = self.parent.maxdetnum

    def run(self):
        newModel = YOLO(
            r'.\ptfolder\best.pt')  # 新建一个专用于保存图像的yolo模型
        if self.nowImageSrc != '':  # 当前正在检测图片
            results = newModel.predict(
                self.nowImageSrc, iou=self.iou, conf=self.conf, max_det=self.maxdetnum, save=True)
        elif self.nowVideoSrc != '':  # 当前正在检测视频
            results = newModel.predict(
                self.nowVideoSrc, iou=self.iou, conf=self.conf, max_det=self.maxdetnum, save=True)


class SaveTxtThread(QThread):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.nowImageSrc = self.parent.nowImageSrc
        self.nowVideoSrc = self.parent.nowVideoSrc
        self.iou = self.parent.iou
        self.conf = self.parent.conf
        self.maxdetnum = self.parent.maxdetnum

    def run(self):
        newModel = YOLO(
            r'.\ptfolder\best.pt')  # 新建一个专用于保存txt的yolo模型
        if self.nowImageSrc != '':  # 当前正在检测图片
            results = newModel.predict(
                self.nowImageSrc, iou=self.iou, conf=self.conf, max_det=self.maxdetnum, save_txt=True, save_conf=True)
        elif self.nowVideoSrc != '':  # 当前正在检测视频
            results = newModel.predict(
                self.nowVideoSrc, iou=self.iou, conf=self.conf, max_det=self.maxdetnum, save_txt=True, save_conf=True)


class SettingWindow(QWidget, Ui_Form2):
    sendValueToMain = Signal(float, float, int)  # 自定义信号，传递变化后的iou conf max_det

    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self.iou = 0.7
        self.conf = 0.25
        self.maxdetnum = 300
        self.setWindowTitle('检测设置')
        self.bind()

    def bind(self):
        self.iouSlider.valueChanged.connect(self.slider2box_iou)
        self.iouSpinBox.valueChanged.connect(self.box2slider_iou)
        self.confSlider.valueChanged.connect(self.slider2box_conf)
        self.confSpinBox.valueChanged.connect(self.box2slider_conf)
        self.numSlider.valueChanged.connect(self.slider2box_num)
        self.numSpinBox.valueChanged.connect(self.box2slider_num)
        self.sendValueToMain.connect(self.parent.rePred)
        self.resetOldSettingButton.clicked.connect(self.resetOldSetting)

    # 滑条变化引起数值变化，同时将变化传回主窗口
    def slider2box_iou(self):
        self.iou = float(self.iouSlider.value()*1.0/100)
        self.iouSpinBox.setValue(self.iou)
        self.sendValueToMain.emit(self.iou, self.conf, self.maxdetnum)

    def slider2box_conf(self):
        self.conf = float(self.confSlider.value()*1.0/100)
        self.confSpinBox.setValue(self.conf)
        self.sendValueToMain.emit(self.iou, self.conf, self.maxdetnum)

    def slider2box_num(self):
        self.maxdetnum = self.numSlider.value()
        self.numSpinBox.setValue(self.maxdetnum)
        self.sendValueToMain.emit(self.iou, self.conf, self.maxdetnum)

    # 数值变化引起滑条变化
    def box2slider_iou(self):
        self.iou = self.iouSpinBox.value()
        self.iouSlider.setValue(int(self.iou*100))

    def box2slider_conf(self):
        self.conf = self.confSpinBox.value()
        self.confSlider.setValue(int(self.conf*100))

    def box2slider_num(self):
        self.maxdetnum = self.numSpinBox.value()
        self.numSlider.setValue(self.maxdetnum)

    # 恢复默认设置
    def resetOldSetting(self):
        self.iou = 0.7
        self.conf = 0.25
        self.maxdetnum = 300
        self.iouSpinBox.setValue(self.iou)
        self.confSpinBox.setValue(self.conf)
        self.numSpinBox.setValue(self.maxdetnum)
        self.iouSlider.setValue(int(self.iou*100))
        self.confSlider.setValue(int(self.conf*100))
        self.numSlider.setValue(self.maxdetnum)
        self.sendValueToMain.emit(self.iou, self.conf, self.maxdetnum)


class ZoomWindow(QWidget, Ui_Form3):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self.setWindowTitle('放大图像')

    def setZoomImage(self, outputImage):
        self.label.setPixmap(self.getScaledQPixmapZoom(outputImage))

    def getScaledQPixmapZoom(self, image):
        return QPixmap(image).scaled(1600, 900, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)


if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
