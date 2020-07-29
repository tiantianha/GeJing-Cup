from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from ui import Ui_Form
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import csv
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
import datetime
import matplotlib.pyplot as plt


def get_picture():
    csvFile = open("1.csv", "r")
    reader = csv.reader(csvFile)
    # 建立空字典
    result = []
    for item in reader:
        if (reader.line_num % 2) != 0:
            # print(item)
            result.append(item)
    csvFile.close()
    Time = datetime.datetime.now()
    Month = int(Time.month)  # 今年要算的月数
    Year = int(Time.year)  # 今年的年份
    Last_Month = 12 - Month  # 上一年要算的月数
    Last_Year = Year - 1  # 上一年的年份
    NightGame = 0  # 熬夜打游戏次数
    Morning = 0
    Noon = 0
    Afternoon = 0
    Evening = 0

    PlayRecord = dict()
    for mon in range(Month):
        PlayRecord[mon + 1] = 0  # 记录今年游戏次数的字典

    Last_PlayRecord = dict()
    for mon in range(Last_Month):
        Last_PlayRecord[mon + Month + 1] = 0  # 记录上一年游戏次数的字典

    for i in result:
        if (int(i[5][0:4]) == Year):  # 2020年的数据
            mon = int(i[5][5:7])  # 获取月份
            PlayRecord[mon] += 1  # 当月打游戏的次数+1
            if (int(i[5][11:13]) >= 22) or (int(i[5][11:13]) <= 6):
                NightGame = NightGame + 1  # 计算熬夜打游戏次数
            if (int(i[5][11:13]) >= 7) and (int(i[5][11:13]) <= 11):
                Morning = Morning + 1
            if (int(i[5][11:13]) >= 11) and (int(i[5][11:13]) <= 13):
                Noon = Noon + 1
            if (int(i[5][11:13]) >= 14) and (int(i[5][11:13]) <= 18):
                Afternoon = Afternoon + 1
            if (int(i[5][11:13]) >= 19) and (int(i[5][11:13]) <= 21):
                Evening = Evening + 1

        if (int(i[5][0:4]) == Last_Year):  # 2019年的数据
            mon = int(i[5][5:7])  # 获取月份
            Last_PlayRecord[mon] += 1
            if (int(i[5][11:13]) >= 22) or (int(i[5][11:13]) <= 6):
                NightGame = NightGame + 1
            if (int(i[5][11:13]) >= 7) and (int(i[5][11:13]) <= 10):
                Morning = Morning + 1
            if (int(i[5][11:13]) >= 11) and (int(i[5][11:13]) <= 13):
                Noon = Noon + 1
            if (int(i[5][11:13]) >= 14) and (int(i[5][11:13]) <= 18):
                Afternoon = Afternoon + 1
            if (int(i[5][11:13]) >= 19) and (int(i[5][11:13]) <= 21):
                Evening = Evening + 1
    # print(PlayRecord)
    # print(Last_PlayRecord)
    # 记录画图所需数据
    x_axis_data = []
    y_axis_data = []
    for key in Last_PlayRecord:
        x_axis_data.append(key)
        y_axis_data.append(Last_PlayRecord[key])
    for key in PlayRecord:
        x_axis_data.append(key)
        y_axis_data.append(PlayRecord[key])

    for i in range(Last_Month):
        x_axis_data[i] = str(Last_Year) + "." + str(x_axis_data[i])
    for i in range(Month):
        x_axis_data[i + Last_Month] = str(Year) + "." + str(x_axis_data[i + Last_Month])

    plt.figure(figsize=(10, 5))
    for a, b in zip(x_axis_data, y_axis_data):
        plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=11)
    plt.bar(x_axis_data, y_axis_data, color="#87CEFA")
    plt.savefig('Figure_1.png')
    plt.show()
    Sum = sum(y_axis_data)
    print("近一年游戏次数:", Sum, "次")
    SumTime = sum(y_axis_data) * 20 / 60  # 英雄联盟对局的最小时间
    print("近一年的至少游戏时间:", SumTime, "小时")
    AverTime = sum(y_axis_data) * 35 / 60  # 英雄联盟对局的平均时间
    print("近一年的平均游戏时间:", AverTime, "小时")
    print("近一年熬夜打游戏次数（22点-6点）:", NightGame, "次")
    PerNightGame = NightGame / Sum
    if PerNightGame > 0.3:
        print("您熬夜打游戏的频率过高，请合理安排时间")
    else:
        print("您熬夜打游戏的频率属于正常范围，继续加油")
    if Sum > 100:
        print("您近一年有游戏上瘾的趋向，请合理安排时间")
    else:
        print("您近一年的游戏时间属于正常范围，继续加油")

    plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文显示
    plt.figure(figsize=(8, 8))  # 将画布设定为正方形，则绘制的饼图是正圆
    label = ['Morning', 'Noon', 'Afternoon', 'Evening', 'Night']  # 定义饼图的标签，标签是列表
    values = [Morning, Noon, Afternoon, Evening, NightGame]
    plt.pie(values, labels=label, autopct='%1.1f%%')  # 绘制饼图
    plt.savefig('Figure_2.png')
    plt.show()


class MyMainWindow(QMainWindow, Ui_Form):   # MyMainWindow类继承QMinWindow和Ui_MinWindow
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)    # 调用父类的构造方法
        self.setupUi(self)
        self.setWindowTitle('英雄联盟游戏沉迷自我分析系统')

        self.model = QStandardItemModel(4, 4)  # 设置数据层次结构，4列

        # 实例化表格视图，设置模型为自定义的模型
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 设置水平方向头标签文本内容
        self.model.setHorizontalHeaderLabels(['召唤师角色', '地图', '游戏模式', '日期'])
        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.tableView)
        self.setLayout(layout)

        dataset = []
        with open('1.csv', 'r') as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                if not row == []:
                    data = [row[0], row[1], row[2], row[5]]
                    dataset.append(data)
        print('dataset is :', dataset)

        for i in range(len(dataset)):
            for j in range(len(dataset[0])):
                temp_data = dataset[i][j]                 # 临时记录，不能直接插入表格
                temp_data = str(temp_data)
                item = QStandardItem(temp_data)
                # 设置每个位置的文本值
                self.model.setItem(i, j, item)
        image = QtGui.QPixmap('Figure_1.png').scaled(self.label.width(), self.label.height())
        self.label.setPixmap(image)
        image2 = QtGui.QPixmap('Figure_2.png').scaled(self.label_2.width(), self.label_2.height())
        self.label_2.setPixmap(image2)


if __name__ == '__main__':
    # get_picture()
    app = QApplication(sys.argv)
    MyWin = MyMainWindow()
    MyWin.show()


    sys.exit(app.exec_())


