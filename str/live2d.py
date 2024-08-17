#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName    :live2d.py
# @Time        :2024/8/15 下午11:51
# @Author      :InubashiriLix
from os import path
import json
from pathlib import Path
import logging
import time
import pyaudio
import struct
import math
import sounddevice as sd
import numpy as np

from PySide6.QtWidgets import (QWidget, QApplication,
                               QLabel, QPushButton,
                               QVBoxLayout, QMenu,
                               QFileDialog, QMessageBox, QInputDialog)
from PySide6.QtCore import Qt, QThread, Signal, QCoreApplication
from PySide6.QtGui import QPixmap, QCursor, QAction


from ui_ConfigWindow import Ui_CONFIG
from ui_voiceSlide import Ui_voiceSlide

# TODO: WRAP THIS SHIT
detection_interval = 0.1
rate = 44100
chunk_size: int = 4096
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=rate,
                input=True,
                frames_per_buffer=chunk_size)


def calculate_volume_norm(indata):
    # 计算样本数据的平方和
    sum_squares = sum(sample ** 2 for sample in indata)
    # 计算均方根值 (RMS)
    rms = math.sqrt(sum_squares / len(indata))
    # 归一化处理，乘以一个因子（与之前的 np.linalg.norm 相当）
    volume_norm = rms * 10
    return volume_norm


def rms_to_db(rms):
    """将RMS转换为分贝(dB)"""
    return 20 * math.log10(rms) if rms > 0 else -math.inf


def _calculate_db(data, _chunk_size) -> float:
    # 将数据转换为16位整数类型
    audio_data = struct.unpack(str(_chunk_size) + 'h', data)

    # 计算音频信号的均方根值 (RMS)
    sum_squares = sum(sample ** 2 for sample in audio_data)
    rms = math.sqrt(sum_squares / _chunk_size)

    # 将RMS转换为分贝值
    db = 20 * math.log10(rms) if rms > 0 else -math.inf
    return db


def d() -> int:
    # 每次检测前加入延迟，减少频率
    time.sleep(detection_interval)
    data = stream.read(chunk_size, exception_on_overflow=False)
    db = _calculate_db(data, chunk_size)
    return int(db)


def actSilD(threshold: int) -> bool:
    return d() >= threshold


class ConfigWindow(QWidget, Ui_CONFIG):
    """
    This Class will be used in Live2D and MainWindow
    in Live2D, it will be used to get the resources path
    in MainWindow, it will used to config
    """

    def __init__(self, parent=None): # the parent should be MainWindow
        super().__init__()
        self.setupUi(self)

        self.parent = parent

        # TODO: def the shit below

        self.configFilePath = Path(__file__).parent / 'config.json'
        self.actPic = QPixmap()
        self.silPic = QPixmap()


        if not self.configFilePath.exists():
            logging.log(logging.INFO, 'config file not found, creating...')
            self.actPicPath, self.silPicPath, self.voiceThreshold = self.runConfig()
            # self.saveToJson() # useless
        else:
            with open(self.configFilePath, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
                activatedPicPath = self.config['activatedPic']
                silentPicPath = self.config['silentPic']
                if not self.checkResourceValidation(actPath=activatedPicPath, silPath=silentPicPath):
                    self.actPicPath, self.silPicPath, self.voiceThreshold = self.runConfig()
                else:
                    self.actPicPath, self.silPicPath, self.voiceThreshold = self.runConfig(True)

        # TODO: def the above shit

        if not self.actPicPath or not self.silPicPath:
            logging.log(logging.INFO, 'config file is invalid, please check...')
            print('111')  # just some test
            raise Exception('config file is invalid, please check...')

        print(self.actPicPath, self.silPicPath)

        # two labels here, one for activated, one for silent,
        # 调整图片大小以适应标签尺寸
        self.labelActPic.setPixmap(
            self.actPic.scaled(self.labelActPic.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.labelSilPic.setPixmap(
            self.silPic.scaled(self.labelSilPic.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # one button for set both Pictures
        self.pushButton.clicked.connect(self.runConfig)
        self.pushButton_2.clicked.connect(lambda: self.setVoiceThreshold())

    def setVoiceThreshold(self):

        def _saveVoiceThresholdToJson(threshold: int):
            # 能运行到这儿一般json文件都解析完了，成了self.config样子的词典了
            print('saving with value {}'.format(threshold))
            self.config['voiceThreshold'] = threshold
            self.voiceThreshold = threshold
            self.saveToJson()

        class VoiceThresholdWindow(QWidget, Ui_voiceSlide):
            def __init__(self, parent: ConfigWindow):
                super().__init__()
                self.setupUi(self)

                self.threshold = parent.voiceThreshold
                self.thresholdSlide.setValue(self.threshold)
                self.thresholdSlide.valueChanged.connect(self.changeThreshold)

                self.VoiceThread1 = VoiceThread1(self)
                self.VoiceThread1.start()

            def changeThreshold(self):
                self.threshold = self.thresholdSlide.value()
                _saveVoiceThresholdToJson(self.threshold)


            def closeEvent(self, event):
                self.VoiceThread1.stop()
                self.VoiceThread1.wait()  # 等待线程结束
                self.VoiceThread1.deleteLater()
                super().closeEvent(event)  # 调用父类的 closeEvent 以确保窗口正常关闭

        class VoiceThread1(QThread):
            def __init__(self, parent: VoiceThresholdWindow = None):
                super().__init__()
                self.is_running = True
                self.parent = parent

            def run(self):
                while self.is_running:
                    db: int = d()
                    self.parent.voiceBar.setValue(db)
                    # print(db)

            def stop(self):
                self.is_running = False

        voiceSetting = VoiceThresholdWindow(self)
        voiceSetting.show()

    @staticmethod
    def checkResourceValidation(actPath: str, silPath: str) -> bool:
        pathAct: bool = Path(actPath).exists()
        pathSil: bool = Path(silPath).exists()
        return pathAct and pathSil

    def saveToJson(self):
        self.parent.config = self.config
        with open(self.configFilePath, 'w', encoding='utf-8') as file:
            json.dump(self.config, file, ensure_ascii=False, indent=4)

    def warningSpring(self, warningInfo):
        reply = QMessageBox.warning(
            self, '警告', warningInfo,
            QMessageBox.Close | QMessageBox.Retry, QMessageBox.Retry)
        if reply == QMessageBox.Close:
            QApplication.instance().quit()  # 退出程序

    def runConfig(self, setupOnly: bool = False) -> (Path, Path, float):
        while True:
            # 获取激活图片路径
            if setupOnly:
                activated_pic = self.config['activatedPic']
            else:
                activated_pic = QFileDialog.getOpenFileName(self, '选择激活图片路径', '.', 'Images (*.png *.jpg)')[0]
                if not activated_pic:  # 如果用户没有选择文件
                    self.warningSpring('没有选择图片，是否要退出程序？')
                    continue  # 重新选择

            # 获取静默图片路径
            if setupOnly:
                silent_pic = self.config['silentPic']
            else:
                silent_pic = QFileDialog.getOpenFileName(self, '选择静默图片路径', '.', 'Images (*.png *.jpg)')[0]
                if not silent_pic:
                    self.warningSpring('没有选择图片，是否要退出程序？')
                    continue  # 重新选择

            # 获取声音阈值
            if setupOnly:
                # 如果配置文件存在或者没有这一配置，则读取配置文件中的阈值
                voiceThreshold = self.config['voiceThreshold']
            else:
                # 如果配置文件不存在，则弹出输入对话框
                voiceThreshold = QInputDialog.getDouble(self, '设置声音阈值', '请输入声音阈值（dB）：', 10.0, 0.0, 100.0)[0]
                if not voiceThreshold:
                    self.warningSpring('没有输入声音阈值，是否要退出程序？')
                    continue

            self.config = {
                'activatedPic': activated_pic,
                'silentPic': silent_pic,
                'voiceThreshold': voiceThreshold
            }

            self.actPic = QPixmap(self.config['activatedPic'])
            self.silPic = QPixmap(self.config['silentPic'])
            self.voiceThreshold = voiceThreshold

            # 检查用户是否选择了有效的文件路径
            actPicPath = Path(self.config['activatedPic'])
            silPicPath = Path(self.config['silentPic'])
            if actPicPath.exists() and silPicPath.exists():
                self.saveToJson()
                return actPicPath, silPicPath, self.voiceThreshold
            else:
                self.warningSpring('选择的文件路径无效，是否要退出程序？')
                return None, None, None

    # api for Live2D
    def returnQPixmap(self) -> (QPixmap, QPixmap):
        if not self.actPic or not self.silPic:
            logging.log(logging.INFO, 'config file is invalid, please check...')
            raise Exception('config file is invalid, please check...')
        return self.actPic, self.silPic


class AudioDetector:
    def __init__(self, threshold):
        self.threshold = threshold
        self.volume_level = 0
        self.is_above_threshold = False

    def audio_callback(self, indata, frames, time, status):
        volume_norm = np.linalg.norm(indata) * 10
        self.volume_level = int(volume_norm)
        self.is_above_threshold = self.volume_level >= self.threshold

class DetectionThread(QThread):
    update_signal = Signal(bool)

    def __init__(self, detector: AudioDetector):
        super().__init__()
        self.detector = detector
        self.is_running = True

    def run(self):
        with sd.InputStream(callback=self.detector.audio_callback):
            while self.is_running:
                self.update_signal.emit(self.detector.is_above_threshold)
                self.msleep(100)  # 参数：线程休眠时间，控制检测频率，单位为毫秒

    def stop(self):
        self.is_running = False
        self.quit()
        self.wait()

class Live2D(QWidget):
    def __init__(self, actPixmap: QPixmap, silPixmap: QPixmap, threshold: int):
        super().__init__()
        self.actPic = actPixmap  # 保持原始大小
        self.silPic = silPixmap  # 保持原始大小
        self.threshold = rms_to_db(threshold)  # 参数：声音阈值，控制声音激活/静默的切换
        self.is_active = False

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)

        self.label_image = QLabel(self)
        self.label_image.setPixmap(self.silPic)
        self.label_image.setFixedSize(self.silPic.size())

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        self.detector = AudioDetector(threshold)
        self.thread = DetectionThread(self.detector)
        self.thread.update_signal.connect(self.update_image)
        self.thread.start()

    def update_image(self, is_active: bool):
        if is_active != self.is_active:
            self.is_active = is_active
            if self.is_active:
                self.label_image.setPixmap(self.actPic)
            else:
                self.label_image.setPixmap(self.silPic)

    def show_context_menu(self, pos):
        context_menu = QMenu(self)
        exit_action = QAction('退出Live2D窗口', self)
        exit_action.triggered.connect(self.close)
        context_menu.addAction(exit_action)
        context_menu.exec(QCursor.pos())

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
        else:
            event.ignore()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.RightButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
        else:
            event.ignore()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            event.accept()
        else:
            event.ignore()

    def closeEvent(self, event):
        self.thread.stop()
        QCoreApplication.quit()
        event.accept()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Lil2D START')
        self.resize(500, 300)

        self.config = None
        self.configPage = ConfigWindow(self)

        self.startButton = QPushButton('Start')
        self.configButton = QPushButton('Config')
        self.bind()

        self.mainLayout = QVBoxLayout()
        self.layoutBind()
        self.setLayout(self.mainLayout)

    def layoutBind(self):
        self.mainLayout.addWidget(self.startButton)
        self.mainLayout.addWidget(self.configButton)

    def bind(self):
        self.startButton.clicked.connect(self.showLive2D)
        self.configButton.clicked.connect(self.configPage.show)

    def showLive2D(self):
        """show live2d and hide mainWindow"""
        self.threshold = self.config['voiceThreshold']

        self.actPic, self.silPic = self.configPage.returnQPixmap()
        self.Live2D = Live2D(self.actPic, self.silPic, threshold=self.threshold)

        self.Live2D.show()
        self.hide()


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()



