from datetime import date
import datetime
import psycopg2
import sys

from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox,
                             QTableWidgetItem, QPushButton, QMessageBox)


curr_date = date.today()
current_date_string = curr_date.strftime('%m,%d,%y')
curr_week = datetime.date(int(current_date_string[6:8]), int(current_date_string[0:2]), int(current_date_string[3:5])).isocalendar().week

#ПОДКЛЮЧЕНИЕ
class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self._connect_to_db()
        self.setWindowTitle("Shedule")
        self.vbox = QVBoxLayout(self)
        self.tabs = QTabWidget(self)#создаёт структуру
        self.vbox.addWidget(self.tabs)

        self._create_shedule_tab()
        self._create_teacher_tab()
        self._create_sub_tab()
        self._create_timetable_tab()


    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="bot", user="postgres", password="PelmeN57a", host="localhost", port="5432")
        self.cursor = self.conn.cursor()

# ВКЛАДКА ПРЕДМЕТЫ
    # Создаём вкладку
    def _create_timetable_tab(self):
        self.timetable_tab = QWidget()#виджет
        self.tabs.addTab(self.timetable_tab, "Timetable")#добавляет виджет

        self.tb_gbox = QGroupBox("Все дни недели")#группирует виджеты(для красоты)

        self.svbox = QVBoxLayout()#вертикаль
        self.shbox1 = QHBoxLayout()#горизонталь
        self.shbox2 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.tb_gbox)

        self._create_tb_table()

        self.update_tb_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_tb_button)
        self.update_tb_button.clicked.connect(self._update_tb)

        self.timetable_tab.setLayout(self.svbox)

# Создаём таблицу
    def _create_tb_table(self):
        self.tb_table = QTableWidget()#пустая таблица
        self.tb_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)#регулирует ячейки

        self.tb_table.setColumnCount(6)
        self.tb_table.setHorizontalHeaderLabels(["Day", "№subject", "Room number", "Start time", "Чётность", " "])

        self._update_tb_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.tb_table)
        self.tb_gbox.setLayout(self.mvbox)

# Выбираем нужное из бд
    def _update_tb_table(self):
        self.cursor.execute("SELECT day, subject, room_numb, start_time, ch FROM timetable")

        records = list(self.cursor.fetchall())

        self.tb_table.setRowCount(len(records) + 1)#задаёт таблице количества строк
        for i, r in enumerate(records):
            r = list(r)

            joinButton = QPushButton("Join")

            self.tb_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.tb_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.tb_table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.tb_table.setItem(i, 3, QTableWidgetItem(str(r[3])))
            self.tb_table.setItem(i, 4, QTableWidgetItem(str(r[4])))
            self.tb_table.setCellWidget(i, 5, joinButton)

            d = 'g'

            joinButton.clicked.connect(lambda ch, num=i: self._change_tb_from_table(num,d))

        self.tb_table.resizeRowsToContents()#адаптирует размеры ячеек

# Обновить данные
    def _change_tb_from_table(self, rowNum, day):
        row = list()
        for i in range(self.tb_table.columnCount()):
            try:
                row.append(self.tb_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute("UPDATE timetable SET room_numb =" + str(int(row[2])) + " WHERE day =" + "'" + str(row[0]) + "'" + " AND subject=" + str(int(row[1])) + " AND start_time =" + "'" + str(row[3]) + "'")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _update_tb(self):
        self._update_tb_table()



# ВКЛАДКА ПРЕДМЕТЫ
# Создаём вкладку
    def _create_sub_tab(self):
        self.sub_tab = QWidget()
        self.tabs.addTab(self.sub_tab, "Subject")

        self.s_gbox = QGroupBox("Предметы")

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.s_gbox)

        self._create_s_table()

        self.update_s_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_s_button)
        self.update_s_button.clicked.connect(self._update_s)

        self.sub_tab.setLayout(self.svbox)

# Создаём таблицу
    def _create_s_table(self):
        self.s_table = QTableWidget()
        self.s_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.s_table.setColumnCount(3)
        self.s_table.setHorizontalHeaderLabels(["№", "Subject", " "])

        self._update_s_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.s_table)
        self.s_gbox.setLayout(self.mvbox)

# Выбираем нужное из бд
    def _update_s_table(self):
        self.cursor.execute("SELECT * FROM subject")

        records = list(self.cursor.fetchall())

        self.s_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)

            joinButton = QPushButton("Join")

            self.s_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.s_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.s_table.setCellWidget(i, 2, joinButton)

            d = 'g'

            joinButton.clicked.connect(lambda ch, num=i: self._change_su_from_table(num, d))

        self.s_table.resizeRowsToContents()

# Обновить данные
    def _change_su_from_table(self, rowNum, day):
        row = list()
        for i in range(self.s_table.columnCount()):
            try:
                row.append(self.s_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute("UPDATE subject SET name_s =" + "'" + str(row[1]) + "'" + "WHERE id_s =" + str(int(row[0])))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _update_s(self):
        self._update_s_table()



#ВКЛАДКА УЧИТЕЛЕЙ
# Создаём вкладку
    def _create_teacher_tab(self):
        self.teacher_tab = QWidget()
        self.tabs.addTab(self.teacher_tab, "Teacher")

        self.teach_gbox = QGroupBox("Преподователи")

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.teach_gbox)

        self._create_teach_table()

        self.update_teach_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_teach_button)
        self.update_teach_button.clicked.connect(self._update_teach)

        self.teacher_tab.setLayout(self.svbox)

# Создаём таблицу
    def _create_teach_table(self):
        self.teach_table = QTableWidget()
        self.teach_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.teach_table.setColumnCount(4)
        self.teach_table.setHorizontalHeaderLabels(["id", "Teacher", "Subject", " "])

        self._update_teach_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.teach_table)
        self.teach_gbox.setLayout(self.mvbox)

# Выбираем нужное из бд
    def _update_teach_table(self):
        self.cursor.execute("SELECT id_t, full_name, name_s FROM teacher INNER JOIN subject ON teacher.sub=subject.id_s")

        records = list(self.cursor.fetchall())

        self.teach_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)

            joinButton = QPushButton("Join")

            self.teach_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.teach_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.teach_table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.teach_table.setCellWidget(i, 3, joinButton)

            d = 'g'

            joinButton.clicked.connect(lambda ch, num=i: self._change_te_from_table(num, d))

        self.teach_table.resizeRowsToContents()

# Обновить данные
    def _change_te_from_table(self, rowNum, day):
        row = list()
        for i in range(self.teach_table.columnCount()):
            try:
                row.append(self.teach_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute("UPDATE teacher SET full_name =" + "'" + str(row[1]) + "'" + "WHERE id_t =" + str(int(row[0])))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")
    def _update_teach(self):
        self._update_teach_table()


#ВКЛАДКА С РАСПИСАНИЕМ НА НЕДЕЛЮ
#Создаём вкладку
    def _create_shedule_tab(self):
        self.shedule_tab = QWidget()
        self.tabs.addTab(self.shedule_tab, "Shedule")

        self.monday_gbox = QGroupBox("Monday")
        self.tuesday_gbox = QGroupBox("Tuesday")
        self.wednesday_gbox = QGroupBox("Wednesday")
        self.thursday_gbox = QGroupBox("Thursday")
        self.friday_gbox = QGroupBox("Friday")
        self.saturday_gbox = QGroupBox("Saturday")

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.monday_gbox)
        self.shbox1.addWidget(self.tuesday_gbox)
        self.shbox1.addWidget(self.wednesday_gbox)
        self.shbox1.addWidget(self.thursday_gbox)
        self.shbox1.addWidget(self.friday_gbox)
        self.shbox1.addWidget(self.saturday_gbox)

        self._create_monday_table()
        self._create_tuesday_table()
        self._create_wednesday_table()
        self._create_thursday_table()
        self._create_friday_table()
        self._create_saturday_table()

        self.update_shedule_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_shedule_button)
        self.update_shedule_button.clicked.connect(self._update_shedule)

        self.shedule_tab.setLayout(self.svbox)

#Создаём каждую таблицу
    def _create_monday_table(self):
        self.monday_table = QTableWidget()
        self.monday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.monday_table.setColumnCount(4)
        self.monday_table.setHorizontalHeaderLabels(["id", "Subject", "Time", " "])

        self._update_monday_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.monday_table)
        self.monday_gbox.setLayout(self.mvbox)

    def _create_tuesday_table(self):
        self.tuesday_table = QTableWidget()
        self.tuesday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.tuesday_table.setColumnCount(4)
        self.tuesday_table.setHorizontalHeaderLabels(["id", "Subject", "Time", " "])

        self._update_tuesday_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.tuesday_table)
        self.tuesday_gbox.setLayout(self.mvbox)

    def _create_wednesday_table(self):
        self.wednesday_table = QTableWidget()
        self.wednesday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.wednesday_table.setColumnCount(4)
        self.wednesday_table.setHorizontalHeaderLabels(["id", "Subject", "Time", " "])

        self._update_wednesday_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.wednesday_table)
        self.wednesday_gbox.setLayout(self.mvbox)

    def _create_thursday_table(self):
        self.thursday_table = QTableWidget()
        self.thursday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.thursday_table.setColumnCount(4)
        self.thursday_table.setHorizontalHeaderLabels(["id", "Subject", "Time", " "])

        self._update_thursday_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.thursday_table)
        self.thursday_gbox.setLayout(self.mvbox)

    def _create_friday_table(self):
        self.friday_table = QTableWidget()
        self.friday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.friday_table.setColumnCount(4)
        self.friday_table.setHorizontalHeaderLabels(["id", "Subject", "Time", " "])

        self._update_friday_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.friday_table)
        self.friday_gbox.setLayout(self.mvbox)

    def _create_saturday_table(self):
        self.saturday_table = QTableWidget()
        self.saturday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.saturday_table.setColumnCount(4)
        self.saturday_table.setHorizontalHeaderLabels(["id", "Subject", "Time", " "])

        self._update_saturday_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.saturday_table)
        self.saturday_gbox.setLayout(self.mvbox)

#Выбираем нужное из бд
    def _update_monday_table(self):
        if curr_week % 2 == 0:
            self.cursor.execute("SELECT subject, name_s, start_time FROM timetable INNER JOIN subject ON timetable.subject=subject.id_s WHERE day='Понедельник' AND ch = 2")
        else:
            self.cursor.execute("SELECT subject, name_s, start_time FROM timetable INNER JOIN subject ON timetable.subject=subject.id_s WHERE day='Понедельник' AND ch = 1")

        records = list(self.cursor.fetchall())

        self.monday_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)

            joinButton = QPushButton("Join")

            self.monday_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.monday_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.monday_table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.monday_table.setCellWidget(i, 3, joinButton)

            d = 'g'

            joinButton.clicked.connect(lambda ch, num=i: self._change_m_from_table(num, d))

        self.monday_table.resizeRowsToContents()

    def _update_tuesday_table(self):
        if curr_week % 2 == 0:
            self.cursor.execute("SELECT subject, name_s, start_time FROM timetable INNER JOIN subject ON timetable.subject=subject.id_s WHERE day='Вторник' AND ch = 2")
        else:
            self.cursor.execute("SELECT subject, name_s, start_time FROM timetable INNER JOIN subject ON timetable.subject=subject.id_s WHERE day='Вторник' AND ch = 1")

        records = list(self.cursor.fetchall())

        self.tuesday_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")

            self.tuesday_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.tuesday_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.tuesday_table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.tuesday_table.setCellWidget(i, 3, joinButton)

            d = 'g'

            joinButton.clicked.connect(lambda ch, num=i: self._change_tu_from_table(num, d))

        self.tuesday_table.resizeRowsToContents()

    def _update_wednesday_table(self):
        if curr_week % 2 == 0:
            self.cursor.execute("SELECT subject, name_s, start_time FROM timetable INNER JOIN subject ON timetable.subject=subject.id_s WHERE day='Среда' AND ch = 2")
        else:
            self.cursor.execute("SELECT subject, name_s, start_time FROM timetable INNER JOIN subject ON timetable.subject=subject.id_s WHERE day='Среда' AND ch = 1")

        records = list(self.cursor.fetchall())

        self.wednesday_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)

            joinButton = QPushButton("Join")

            self.wednesday_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.wednesday_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.wednesday_table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.wednesday_table.setCellWidget(i, 3, joinButton)

            d = 'g'

            joinButton.clicked.connect(lambda ch, num=i: self._change_w_from_table(num, d))

        self.wednesday_table.resizeRowsToContents()

    def _update_thursday_table(self):
        if curr_week % 2 == 0:
            self.cursor.execute("SELECT subject, name_s, start_time FROM timetable INNER JOIN subject ON timetable.subject=subject.id_s WHERE day='Четверг' AND ch = 2")
        else:
            self.cursor.execute("SELECT subject, name_s, start_time FROM timetable INNER JOIN subject ON timetable.subject=subject.id_s WHERE day='Четверг' AND ch = 1")

        records = list(self.cursor.fetchall())

        self.thursday_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)

            joinButton = QPushButton("Join")

            self.thursday_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.thursday_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.thursday_table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.thursday_table.setCellWidget(i, 3, joinButton)

            d = 'g'

            joinButton.clicked.connect(lambda ch, num=i: self._change_th_from_table(num, d))

        self.thursday_table.resizeRowsToContents()

    def _update_friday_table(self):
        if curr_week % 2 == 0:
            self.cursor.execute("SELECT subject, name_s, start_time FROM timetable INNER JOIN subject ON timetable.subject=subject.id_s WHERE day='Пятница' AND ch = 2")
        else:
            self.cursor.execute("SELECT subject, name_s, start_time FROM timetable INNER JOIN subject ON timetable.subject=subject.id_s WHERE day='Пятница' AND ch = 1")

        records = list(self.cursor.fetchall())

        self.friday_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)

            joinButton = QPushButton("Join")

            self.friday_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.friday_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.friday_table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.friday_table.setCellWidget(i, 3, joinButton)

            d = 'g'

            joinButton.clicked.connect(lambda ch, num=i: self._change_f_from_table(num, d))

        self.friday_table.resizeRowsToContents()

    def _update_saturday_table(self):
        if curr_week % 2 == 0:
            self.cursor.execute("SELECT subject, name_s, start_time FROM timetable INNER JOIN subject ON timetable.subject=subject.id_s WHERE day='Суббота' AND ch = 2")
        else:
            self.cursor.execute("SELECT subject, name_s, start_time FROM timetable INNER JOIN subject ON timetable.subject=subject.id_s WHERE day='Суббота' AND ch = 1")

        records = list(self.cursor.fetchall())

        self.saturday_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)

            joinButton = QPushButton("Join")

            self.saturday_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.saturday_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.saturday_table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.saturday_table.setCellWidget(i, 3, joinButton)

            d = 'g'

            joinButton.clicked.connect(lambda ch, num=i: self._change_s_from_table(num, d))

        self.saturday_table.resizeRowsToContents()

#Обновить данные
    def _change_m_from_table(self, rowNum, day):
        row = list()
        for i in range(self.monday_table.columnCount()):
            try:
                row.append(self.monday_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute("UPDATE subject SET name_s =" + "'" + str(row[1]) + "'" + "WHERE id_s =" + str(int(row[0])))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _change_tu_from_table(self, rowNum, day):
        row1 = list()
        for i in range(self.tuesday_table.columnCount()):
            try:
                row1.append(self.tuesday_table.item(rowNum, i).text())
            except:
                row1.append(None)
        try:
            self.cursor.execute("UPDATE subject SET name_s =" + "'" + str(row1[1]) + "'" + "WHERE id_s =" + str(int(row1[0])))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _change_w_from_table(self, rowNum, day):
        row2 = list()
        for i in range(self.wednesday_table.columnCount()):
            try:
                row2.append(self.wednesday_table.item(rowNum, i).text())
            except:
                row2.append(None)
        try:
            self.cursor.execute("UPDATE subject SET name_s =" + "'" + str(row2[1]) + "'" + "WHERE id_s =" + str(int(row2[0])))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _change_th_from_table(self, rowNum, day):
        row3 = list()
        for i in range(self.thursday_table.columnCount()):
            try:
                row3.append(self.thursday_table.item(rowNum, i).text())
            except:
                row3.append(None)
        try:
            self.cursor.execute("UPDATE subject SET name_s =" + "'" + str(row3[1]) + "'" + "WHERE id_s =" + str(int(row3[0])))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _change_f_from_table(self, rowNum, day):
        row4 = list()
        for i in range(self.friday_table.columnCount()):
            try:
                row4.append(self.friday_table.item(rowNum, i).text())
            except:
                row4.append(None)
        try:
            self.cursor.execute("UPDATE subject SET name_s =" + "'" + str(row4[1]) + "'" + "WHERE id_s =" + str(int(row4[0])))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _change_s_from_table(self, rowNum, day):
        row5 = list()
        for i in range(self.saturday_table.columnCount()):
            try:
                row5.append(self.saturday_table.item(rowNum, i).text())
            except:
                row5.append(None)
        try:
            self.cursor.execute("UPDATE subject SET name_s =" + "'" + str(row5[1]) + "'" + "WHERE id_s =" + str(int(row5[0])))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")


#Обновить саму страницу
    def _update_shedule(self):
        self._update_monday_table()
        self._update_tuesday_table()
        self._update_wednesday_table()
        self._update_thursday_table()
        self._update_friday_table()
        self._update_saturday_table()
        self._update_teach_table()


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())