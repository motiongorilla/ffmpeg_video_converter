import sys
import subprocess
import os
import logic
from converter_ui import Ui_MainWindow

from PyQt6 import QtCore, QtGui, QtWidgets


class videoConverter(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        # Initial setup
        super(videoConverter, self).__init__()
        self.setupUi(self)
        self.sourceFileName = None
        self.outputFileName = None
        self.codecDict: dict = {
            "x264": "libx264",
            "x265": "libx265",
            "ProRes": "prores_ks",
            "gif": "gif",
        }
        self.bitratesDict: dict = {
            "Constant bitrate": "crf",
            "Variable bitrate": "pass",
        }
        self.constant = True
        self.variable = False
        self.resolutionList = [
            "360x800",
            "360x720",
            "1280x720",
            "1920x1080",
            "1080x1920",
            "2560x1440",
            "4096x2160",
        ]
        self.crfDict: dict = {
            "Loseless": 0,
            "Best quality": 8,
            "High quality": 25,
            "Medium quality": 33,
            "Low quality": 46,
            "Worst quality": 51,
        }
        # Defaults
        self.le_ffmpegPath.setText(logic.ffmpeg)
        self.le_ffmpegPath.setReadOnly(True)
        self.le_fileToConvertPath.setReadOnly(True)
        self.le_savePath.setReadOnly(True)
        self.cb_constantBitrateSpeed.setCurrentIndex(5)
        self.cb_constatBitrateQuality.setCurrentIndex(2)

        # Buttons connection
        self.btn_ffmpegExplore.clicked.connect(self.findFfmpeg)
        self.btn_filToConvertExplore.clicked.connect(self.getFileToConvert)
        self.btn_saveFilePath.clicked.connect(self.setDestinationPath)
        self.cb_bitrateType.currentIndexChanged.connect(self.hideBitrateSetting)
        self.chb_resize.toggled.connect(self.enableResolution)
        self.chb_customSize.toggled.connect(self.enableResolution)
        self.btn_start.clicked.connect(self.startEncode)

        self.setupCodecList()
        self.setupBitrateList()
        self.setupResolutionList()

    def findFfmpeg(self):
        dialog = QtWidgets.QFileDialog()
        path = dialog.getOpenFileName(self, "ffmpeg", "/usr/")
        self.le_ffmpegPath.setText(path[0])

    def getFileToConvert(self):
        dialog = QtWidgets.QFileDialog()
        path = dialog.getOpenFileName(self, "File to convert", "")
        self.le_fileToConvertPath.setText(path[0])
        fileName = os.path.split(path[0])[1]
        self.sourceFileName = os.path.splitext(fileName)[0]

    def setDestinationPath(self):
        dialog = QtWidgets.QFileDialog()
        path = dialog.getExistingDirectory(self, "Destination path")
        self.le_savePath.setText(path)

        src_path = os.path.split(self.le_fileToConvertPath.text())[0]
        if src_path == path:
            self.outputFileName = f"{self.sourceFileName}_converted"
            return
        self.outputFileName = self.sourceFileName

    def setupCodecList(self):
        self.lw_codecs.clear()
        codecs = self.codecDict.keys()
        self.lw_codecs.addItems(codecs)
        self.lw_codecs.setCurrentItem(self.lw_codecs.item(1))

    def setupBitrateList(self):
        list = self.bitratesDict.keys()
        self.cb_bitrateType.clear()
        self.cb_bitrateType.addItems(list)

    def hideBitrateSetting(self):
        entries = self.cb_bitrateType.count()
        if entries < 2:
            return

        currIndex = self.cb_bitrateType.currentIndex()
        if currIndex == 0:
            self.constant = False
            self.variable = True
        else:
            self.constant = True
            self.variable = False

        self.lb_constantBitrateQualityabel.setHidden(self.constant)
        self.cb_constantBitrateSpeed.setHidden(self.constant)
        self.cb_constatBitrateQuality.setHidden(self.constant)
        self.sb_variableBitrateValue.setHidden(self.variable)
        self.lb_variableBitrateLabel.setHidden(self.variable)

    def setupResolutionList(self):
        self.cb_resolution.clear()
        self.cb_resolution.addItems(self.resolutionList)
        self.cb_resolution.setCurrentIndex(3)
        self.enableResolution()

    def enableResolution(self):
        state = not self.chb_resize.isChecked()
        customState = self.chb_customSize.isChecked()
        listState = state
        if customState:
            listState = False
        self.cb_resolution.setEnabled(listState)
        self.chb_customSize.setEnabled(state)
        self.sb_resoX.setEnabled(customState)
        self.sb_resoY.setEnabled(customState)

    def assembleCommand(self):
        file = ["-i", self.le_fileToConvertPath.text()]

        codecItem: QtWidgets.QListWidgetItem = self.lw_codecs.currentItem()
        codec = ["-c:v", self.codecDict[codecItem.text()]]

        speed = ["-preset", self.cb_constantBitrateSpeed.currentText()]
        crf = ["-crf", self.crfDict[self.cb_constatBitrateQuality.currentText()]]

        resolution = ["-s", self.cb_resolution.currentText()]

        audioSetting = ["-c:a", "copy"]
        convertedName = str(self.outputFileName) + self.cb_fileFormat.currentText()

        output = os.path.join(self.le_savePath.text(), convertedName)
        commands: list = []

        x26n_commands: list = [
            self.le_ffmpegPath.text(),
            file,
            codec,
            speed,
            crf,
            output,
        ]

        for c in x26n_commands:
            if isinstance(c, list):
                for cmd in c:
                    commands.append(str(cmd))
            else:
                commands.append(c)

        return commands

        # "-pix_fmt",
        # "yuv420p",

    def startEncode(self):
        print(self.assembleCommand())
        if subprocess.run(self.assembleCommand()).returncode == 0:
            print("Success!")
        else:
            print("Fail!")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = videoConverter()
    window.show()

    sys.exit(app.exec())
