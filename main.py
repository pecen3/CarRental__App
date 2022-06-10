import sys
from cgitb import text

import pypyodbc as p
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QComboBox

from test import Ui_Form

con = p.connect('DRIVER={SQL Server};SERVER=vm-as35.staff.corp.local;'
                'DATABASE=db_Skroba;UID=student;PWD=sql2020')


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.comboBox.activated.connect(self.checkCombobox1)
        self.ui.comboBox_2.activated.connect(self.checkCombobox2)


    def loaddata(self, Name, Column, Row, Head):
        cursor = con.cursor()
        cursor.execute(f'select * from {Name}')
        row = cursor.fetchone()
        tablerow = 0
        self.ui.tableWidget.setColumnCount(Column)
        self.ui.tableWidget.setRowCount(Row)
        self.ui.tableWidget.verticalHeader().hide()
        self.ui.tableWidget.setHorizontalHeaderLabels(Head)
        while row is not None:
            for i in range(Column):
                self.ui.tableWidget.setItem(tablerow, i,
                                            QtWidgets.QTableWidgetItem(
                                                str(row[i])))
            row = cursor.fetchone()
            tablerow += 1

    def checkboxall(self):
        self.ui.comboBox.activated.connect(self.checkCombobox1)
        self.ui.comboBox_2.activated.connect(self.checkCombobox2)


    def Client(self):
        self.loaddata("Client", 10, 10,
                      ["Client_ID", "Last_Name", "Name", "Middle_Name",
                       "Passport_Details", "License", "Experience",
                       "Phone_Number",
                       "Residence_Place", "Birth_Date"])

    def Bill(self):
        self.loaddata("Bill", 3, 10,
                      ["Res_ID", "Total_Amount", "Total_Mileage"])
    def Make(self):
        self.loaddata("Make", 1, 10, ["Make_Name"])
        self.ui.pushButton.clicked.connect(self.make_insert)

    def Place(self):
        self.loaddata("Place", 2, 10,
                      ["Place_ID", "Name_Place"])
        self.ui.pushButton_2.clicked.connect(self.place_delete)


    def checkCombobox1(self):
        if self.ui.comboBox.currentText() == "Client":
            self.ui.tableWidget.clear()
            self.Client()
        elif self.ui.comboBox.currentText() == "Bill":
            self.ui.tableWidget.clear()
            self.Bill()
        elif self.ui.comboBox.currentText() == "Make":
            self.ui.tableWidget.clear()
            self.Make()
        elif self.ui.comboBox.currentText() == "Place":
            self.ui.tableWidget.clear()
            self.Place()

    def checkCombobox2(self):
        if self.ui.comboBox_2.currentText() == "Клиенты с ДТП":
            self.ui.tableWidget.clear()
            self.Accident_Clients()
        elif self.ui.comboBox_2.currentText() == "Машины “Volkswagen“":
            self.ui.tableWidget.clear()
            self.AutoVolks()
        else:
            self.ui.tableWidget.clear()
            self.TopAuto()

    def Accident_Clients(self):
        cursor = con.cursor()
        cursor.execute(
            "select Client.Last_Name, Client.Name, Client.Middle_Name, count(*) "
            "from Client inner join Reservation on Client.Client_ID = Reservation.Client_ID "
            "where Reservation.Accident_ID > 0 "
            "group by Client.Last_Name, Client.Name, Client.Middle_Name "
            "order by count(*) desc")
        row = cursor.fetchone()
        tablerow = 0
        self.ui.tableWidget.setColumnCount(4)
        self.ui.tableWidget.setRowCount(10)
        self.ui.tableWidget.verticalHeader().hide()
        self.ui.tableWidget.setHorizontalHeaderLabels(
            ["Фамилия", "Имя", "Отчество", "Количество ДТП"])
        while row is not None:
            for i in range(4):
                self.ui.tableWidget.setItem(tablerow, i,
                                            QtWidgets.QTableWidgetItem(
                                                str(row[i])))
            row = cursor.fetchone()
            tablerow += 1


    def AutoVolks(self):
        cursor = con.cursor()
        cursor.execute("select * "
                       "from Car c inner join Model m on c.Model_Name = m.Model_Name "
                       "where m.Make_Name = 'Volkswagen' ")
        row = cursor.fetchone()
        tablerow = 0
        self.ui.tableWidget.setColumnCount(13)
        self.ui.tableWidget.setRowCount(10)
        self.ui.tableWidget.verticalHeader().hide()
        self.ui.tableWidget.setHorizontalHeaderLabels(
            ["Car_ID", "Model_Name ", "Release_Year",
             "Color", "Mileage", "Transmission",
             "Registration_Number", "Vin", "Cost_Per_Day", "Car_Type",
             "Person_Capacity", "Luggage_Capacity", "Status_Value"])
        while row is not None:
            for i in range(13):
                self.ui.tableWidget.setItem(tablerow, i,
                                            QtWidgets.QTableWidgetItem(
                                                str(row[i])))
            row = cursor.fetchone()
            tablerow += 1

    def TopAuto(self):
        cursor = con.cursor()
        cursor.execute("Select top 3 m.Make_Name, m.Model_Name, count(*) "
                       "from Reservation r inner join Car c on r.Car_ID = c.Car_ID "
                       "inner join Model m on m.Model_Name = c.Model_Name "
                       "group by m.Make_Name, m.Model_Name "
                       "order by count(*) desc ")
        row = cursor.fetchone()
        tablerow = 0
        self.ui.tableWidget.setColumnCount(3)
        self.ui.tableWidget.setRowCount(3)
        self.ui.tableWidget.verticalHeader().hide()
        self.ui.tableWidget.setHorizontalHeaderLabels(
            ["Марка", "Модель", "Забронированно раз"])
        while row is not None:
            for i in range(3):
                self.ui.tableWidget.setItem(tablerow, i,
                                            QtWidgets.QTableWidgetItem(
                                                str(row[i])))
            row = cursor.fetchone()
            tablerow += 1

    def make_insert(self):
        cursor = con.cursor()
        cursor.execute("insert into Make (Make_Name) values ('%s')" % (''.join(self.ui.lineEdit.text())))
        QMessageBox.about(self, 'Успешно', 'Данные добавлены в таблицу!')
        cursor.commit()
        self.Make()


    def place_delete(self):
        cursor = con.cursor()
        cursor.execute(f'delete from Place where Place_ID = {int(self.ui.lineEdit.text())}')
        QMessageBox.about(self, 'Успешно', 'Данные удалены из таблицы!')
        cursor.commit()
        self.Place()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())

    # def loaddata(self, Name, Column, Row, Head):
    #     cursor = con.cursor()
    #     cursor.execute(f'select * from {Name}')
    #     row = cursor.fetchone()
    #     tablerow = 0
    #     self.tableWidget.setColumnCount(Column)
    #     self.tableWidget.setRowCount(Row)
    #     self.tableWidget.verticalHeader().hide()
    #     self.tableWidget.setHorizontalHeaderLables(Head)
    #     while row is not None:
    #         for i in range(Column):
    #             self.tableWidget.setItem(tablerow, i,
    #                                      QtWidgets.QTableWidget(str(row[i])))
    #         row = cursor.fetchone()
    #         tablerow += 1
