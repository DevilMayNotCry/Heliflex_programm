import sys, design
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from .db import db_connection, select_params
from .sensor import serial_connection
from .settings import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, TABLE_NAME, SERIAL_PORT, BAUNDRATE


class HeliflexApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        self.coil_count = 0
        self.length_temp = 0
        """Инициализация соединения с базой данных и сплатой"""
        self.cursor = db_connection(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
        self.ser = serial_connection(SERIAL_PORT, BAUNDRATE)
        """Подгрузка интерфейса пользователя"""
        super().__init__()
        self.setupUi(self)
        result = select_params(self.cursor, '*', TABLE_NAME)
        for i in result:
            self.cmbProduct.addItem(str(i[0]))
        self.cmbProduct.activated.connect(self.values)
        self.qTimer = QTimer()
        self.qTimer.setInterval(3000)
        self.qTimer.timeout.connect(self.getSensorValue)
        self.qTimer.start()
        self.butCounterReset.clicked.connect(self.reset)

    def values(self):
        """Получение данных из бд и заполнение полей"""
        result = select_params(self.cursor, self.cmbProduct.currentText(), TABLE_NAME)
        self.lblPVC.setText(str(result[0]))
        self.lblWiresL.setText(str(result[1]))
        self.lblWiresLQ.setText(str(result[2]))
        self.lblWiresC.setText(str(result[3]))
        self.lblWiresCQ.setText(str(result[4]))
        self.lblDiaO.setText(str(result[5]))
        self.lblDiaI.setText(str(result[6]))
        self.lblThickness.setText(str(result[7]))
        self.lblWeigh.setText(str(result[8]))
        self.lblPitch.setText(str(result[9]))

    def reset(self):
        """Сброс счетчика бухт"""
        self.coil_count = 0
        self.lbl_coilCounter.setText('0')

    def getSensorValue(self):
        """Получения значений от датчиков"""
        line_sum = ""
        ser.write(b's')
        for i in range(4):
            for line in ser.readline():
                if line != 10:
                        line_sum = line_sum + chr(line)
                else:
                    print(line_sum)
            if line_sum[0] == 'a':
                if float(line_sum[1:]) != 0:
                    rpm_1 = round(60000 / float(line_sum[1:]), 2)
                else:
                    rpm_1 = 0.1
                self.lbl_rpm1.setText(str(rpm_1))
            if line_sum[0] == 'b':
                if float(line_sum[1:]) != 0:
                    rpm_2 = round(60000 / float(line_sum[1:]), 2)
                else:
                    rpm_2 = 0.1
                self.lbl_rpm2.setText(str(rpm_2))
            if line_sum[0] == 'c':
                if float(line_sum[1:]) != 0:
                    rpm = round(600 / float(line_sum[1:]), 2)
                else:
                    rpm = 0
                mm_min = round(0.7536 * rpm, 1)
                self.lbl_rpm.setText(str(rpm))
                self.lbl_mmmin.setText(str(mm_min))
            if line_sum[0] == 'd':
                self.lbl_counter.setText(line_sum[1:])
                if self.length_temp > float(line_sum[1:]):
                    self.coil_count = self.coil_count + 1
                    self.lbl_coilCounter.setText(str(self.coil_count))
                self.length_temp = float(line_sum[1:])
            line_sum = ''
        pitch = round((1000 * mm_min) / ((rpm_1 + rpm_2) / 2), 1)
        self.lbl_pitch.setText(str(pitch))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = HeliflexApp()
    window.show()
    app.exec_()
