from os import replace
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QTabWidget, QApplication, QHBoxLayout, QTextEdit, QToolButton, QMessageBox, QVBoxLayout, QLineEdit, QMenu, QAction
from PyQt5.Qt import QIcon
import Baidu
from PyQt5 import QtCore
import sys

class tranHelper(QWidget):
    def __init__(self):
        super().__init__()
        self.ontop = 0
        self.getStyle()
        self.iniUI()

    def getStyle(self):
        try:
            with open('./resources/qss/style.css') as file:
                self.style = file.read()
        except:
            print('未能成功加载样式!')

    def iniUI(self):
        self.setWindowTitle('翻译助手')
        window_icon = QIcon('./resources/images/icon.png')
        self.setWindowIcon(window_icon) # 设置图标
        self.resize(600, 400)

        # translate layout
        self.tran_layout = QHBoxLayout()
        self.tran_h_layout = QHBoxLayout()
        self.tran_v_layout = QVBoxLayout()

        # translate items
        self.text1 = QTextEdit()
        self.text1.setPlaceholderText('输入原文...')
        self.text2 = QTextEdit()
        self.text2.setPlaceholderText('翻译后的文章...')
        self.clear_button = QPushButton('清空')
        self.translate_button = QPushButton('翻译')
        self.ontop_button = QPushButton('置顶')

        self.clear_button.setProperty('name', 'clear_button')
        self.translate_button.setProperty('name', 'translate_button')
        self.ontop_button.setProperty('name', 'ontop_button')

        # set tip
        self.clear_button.setToolTip('清空快捷键Alt+C')
        self.translate_button.setToolTip('翻译快捷键Alt+T')

        # add layout
        self.tran_h_layout.addWidget(self.text1)
        self.tran_h_layout.addWidget(self.text2)
        self.tran_v_layout.addWidget(self.translate_button)
        self.tran_v_layout.addWidget(self.clear_button)
        self.tran_v_layout.addStretch(4)
        self.tran_v_layout.addWidget(self.ontop_button)
        self.tran_h_layout.addLayout(self.tran_v_layout)
        self.tran_layout.addLayout(self.tran_h_layout)

        # translate page
        self.tran_frame = QWidget()
        self.replace_frame = QWidget()
        

        # replace page
        self.replace_text = QTextEdit()
        self.read_replace_text()

        # replace layout
        self.replace_layout = QHBoxLayout()
        self.replace_layout.addWidget(self.replace_text)

        # set frame layout
        self.tran_frame.setLayout(self.tran_layout)
        self.replace_frame.setLayout(self.replace_layout)
        

        # set tab
        self.icon1 = QIcon('./resources/images/pen.png')
        self.icon2 = QIcon('./resources/images/docx.png')

        self.tab = QTabWidget()
        self.tab.resize(300, 250)
        self.tab.setTabPosition(QTabWidget.West)
        self.tab.setIconSize(QtCore.QSize(32, 32))
        self.tab.addTab(self.tran_frame, self.icon1, '')
        self.tab.addTab(self.replace_text, self.icon2, '')

        # frame
        self.frame = QHBoxLayout()
        self.frame.addWidget(self.tab)
        self.setLayout(self.frame)

        # button function
        self.translate_button.clicked.connect(self.translate_function)
        self.clear_button.clicked.connect(self.clear_function)
        self.ontop_button.clicked.connect(self.ontop_function)

        # set shortcut
        self.translate_button.setShortcut('Alt+T')
        self.clear_button.setShortcut('Alt+C')

        self.setStyleSheet(self.style)

        self.show()

    def read_replace_text(self):
        try:
            with open('./replace.txt', 'r') as file:
                text = file.read()
            
            self.replace_text.setText(text)
        except:
            print('Read file error!')
            self.info('读文件错误!')

    # operate the original
    def operate(self, original):
        result = ''
        replace_cmd = ''
        for cmd in self.replace_text.toPlainText().split('\n'):
            if (cmd != ''):
                replace_cmd = replace_cmd + '.' + cmd

        # print(replace_cmd)
        # print('"' + original + '"' + replace_cmd)
        # print("'''" + original + "'''" + replace_cmd)
        # print(eval("'''" + original + "'''" + replace_cmd))
        try:
            return (eval("'''" + original + "'''" + replace_cmd))
        except:
            self.info('replace命令出错')
            return ('replace命令出错')

    # clear function
    def clear_function(self):
        self.text1.setText('')
        self.text2.setText('')

    # translate function
    def translate_function(self):
        original = self.text1.toPlainText()
        # print(original)
        result = self.operate(original = original)
        print(result)

        try:
            if (result != 'replace命令出错'):
                trans = Baidu.getJson(result)
                json = trans.fetch_json()

                print(json['trans_result']['data'][0]['dst'])
                self.text2.setText(json['trans_result']['data'][0]['dst'])
        except:
            self.info('翻译出错')

    # on top function
    def ontop_function(self):
        if self.ontop == 0:
            self.ontop = 1
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.ontop_button.setText('已置顶')
        elif self.ontop == 1:
            self.ontop = 0
            self.setWindowFlags(QtCore.Qt.Widget)
            self.ontop_button.setText('置顶')
        self.show()

    # info
    def info(self, information):
        reply = QMessageBox.information(self, '提示', information, QMessageBox.Close, QMessageBox.Close)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = tranHelper()
    sys.exit(app.exec_())