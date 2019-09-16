from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import sys
import os
from sys import platform
import mysql.connector
from mysql.connector import errorcode
from mysql.connector.errors import Error
import tkinter as tk
import ctypes
from tkinter import messagebox

root = tk.Tk()
wpx = root.winfo_screenwidth()
hpx = root.winfo_screenheight()

if platform == 'win32':
    userwin = ctypes.windll.user32
    userwin.SetProcessDPIAware()
    [w, h] = [userwin.GetSystemMetrics(0), userwin.GetSystemMetrics(1)]
    cdpi = w*96/wpx
elif platform == 'darwin':
    usermac = ctypes.cdll.kernel32
    usermac.SetProcessDPIAware()
    [w, h] = [usermac.GetSystemMetrics(0), usermac.GetSystemMetrics(1)]
    cdpi = w*96/wpx
    from Foundation import NSBundle
    bundle = NSBundle.mainBundle()
    if bundle:
        info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
        if info and info['CFBundleName'] == 'Python':
            info['CFBundleName'] = 'MySQL Explorer'

root.withdraw()

class Invalid(Exception):
    pass

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        w1 = w/10*7
        h1 = h/10*7
        MainWindow.setGeometry(QtCore.QRect(w/5 - (w1/14), h/5 - (h1/14), w1, h1))
        MainWindow.setMinimumSize(w1, h1)
        MainWindow.setDocumentMode(False)
        MainWindow.setDockNestingEnabled(False)

        width = MainWindow.frameGeometry().width()
        height = MainWindow.frameGeometry().height()
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.mysqlExplorer = QtWidgets.QTabWidget(self.centralwidget)
        self.mysqlExplorer.setGeometry(QtCore.QRect(0, 0, width, height))
        self.mysqlExplorer.setObjectName("mysqlExplorer")
        
        self.LoginPage = QtWidgets.QWidget()
        self.LoginPage.setObjectName("LoginPage")
        self.mysqlExplorer.addTab(self.LoginPage, "Login Page")
        
        self.Explorer = QtWidgets.QWidget()
        self.Explorer.setObjectName("Explorer")
        self.mysqlExplorer.addTab(self.Explorer, "Explorer")

        widthL = self.mysqlExplorer.frameGeometry().width()/10 * 5
        heightL = self.mysqlExplorer.frameGeometry().height()/10 * 5

        w2 = cdpi/80
        w3 = hpx/432
        
        self.unameLabel = QtWidgets.QLabel(self.LoginPage)
        self.unameLabel.setObjectName("unameLabel")
        self.unameLabel.setScaledContents(True)
        self.unameLabel.setGeometry(QtCore.QRect(widthL - self.unameLabel.width() * w2, heightL - (cdpi/11) * 6.5, self.unameLabel.width(), (cdpi/11) * w3))

        self.uname = QtWidgets.QLineEdit(self.LoginPage)
        self.uname.setObjectName("uname")
        self.uname.setPlaceholderText("Username")
        self.uname.setGeometry(QtCore.QRect(widthL - (self.unameLabel.frameGeometry().width() * 2.5)/6, heightL - (cdpi/11) * 6.5, self.unameLabel.frameGeometry().width() * (w2*2), (cdpi/11) * w3))
        
        self.upassLabel = QtWidgets.QLabel(self.LoginPage)
        self.upassLabel.setObjectName("upassLabel")
        self.upassLabel.setScaledContents(True)
        self.upassLabel.setGeometry(QtCore.QRect(widthL - self.upassLabel.width() * w2, heightL - (cdpi/11) * 3.5, self.upassLabel.width(), (cdpi/11) * w3))
             
        self.upass = QtWidgets.QLineEdit(self.LoginPage)
        self.upass.setObjectName("upass")
        self.upass.setPlaceholderText("Password")
        self.upass.setEchoMode(self.upass.Password)
        self.upass.setGeometry(QtCore.QRect(widthL - (self.unameLabel.frameGeometry().width() * 2.5)/6, heightL - (cdpi/11) * 3.5, self.unameLabel.frameGeometry().width() * (w2*2), (cdpi/11) * w3))
        
        self.hostLabel = QtWidgets.QLabel(self.LoginPage)
        self.hostLabel.setObjectName("hostLabel")
        self.hostLabel.setScaledContents(True)
        self.hostLabel.setGeometry(QtCore.QRect(widthL - self.hostLabel.width() * w2, heightL - (cdpi/11) * 0.5, self.hostLabel.width(), (cdpi/11) * w3))
        
        self.uhost = QtWidgets.QLineEdit(self.LoginPage)
        self.uhost.setObjectName("uhost")
        self.uhost.setPlaceholderText("Local Host is 127.0.0.1")
        self.uhost.setGeometry(QtCore.QRect(widthL - (self.unameLabel.frameGeometry().width() * 2.5)/6, heightL - (cdpi/11) * 0.5, self.unameLabel.frameGeometry().width() * (w2*2), (cdpi/11) * w3))
        
        self.uportLabel = QtWidgets.QLabel(self.LoginPage)
        self.uportLabel.setObjectName("uportLabel")
        self.uportLabel.setScaledContents(True)
        self.uportLabel.setGeometry(QtCore.QRect(widthL - self.uportLabel.width() * w2, heightL + (cdpi/11) * 2.5, self.uportLabel.width(), (cdpi/11) * w3))
        
        self.uport = QtWidgets.QLineEdit(self.LoginPage)
        self.uport.setObjectName("uport")
        self.uport.setPlaceholderText("Default Port is 3306")
        self.uport.setGeometry(QtCore.QRect(widthL - (self.unameLabel.frameGeometry().width() * 2.5)/6, heightL + (cdpi/11) * 2.5, self.unameLabel.frameGeometry().width() * (w2*2), (cdpi/11) * w3))

        self.DropDownLabel = QtWidgets.QLabel(self.LoginPage)
        self.DropDownLabel.setObjectName("DropDownLabel")
        self.DropDownLabel.setScaledContents(True)
        self.DropDownLabel.setGeometry(QtCore.QRect(widthL - self.DropDownLabel.width() * w2, heightL + (cdpi/2), self.DropDownLabel.width() + 2, (cdpi/11) * w3))

        self.DropDown = QtWidgets.QComboBox(self.LoginPage)
        self.DropDown.setObjectName("DropDown")
        self.DropDown.setGeometry(QtCore.QRect(widthL - (self.unameLabel.frameGeometry().width() * 2.5)/6, heightL + (cdpi/2), self.unameLabel.frameGeometry().width() * (w2*2), (cdpi/11) * w3))
        
        self.SaveLogin = QtWidgets.QCheckBox(self.LoginPage)
        self.SaveLogin.setObjectName("SaveLogin")
        self.SaveLogin.setGeometry(QtCore.QRect(widthL -  110* w2, heightL + (cdpi/11) * 9, 120, (cdpi/11) * (w3/1.66)))
        
        self.LoginButton = QtWidgets.QPushButton(self.LoginPage)
        self.LoginButton.setObjectName("LoginButton")
        self.LoginButton.setAutoDefault(True)
        self.LoginButton.setGeometry(QtCore.QRect(widthL - (self.unameLabel.frameGeometry().width() * 2.5)/6, heightL + (cdpi/11) * 8.5, self.unameLabel.frameGeometry().width() * (w2*2), (cdpi/11) * w3))

        self.MysqlImage = QtWidgets.QLabel(self.LoginPage)
        self.MysqlImage.setText("")
        self.MysqlImage.setPixmap(QtGui.QPixmap("logo.png"))
        self.MysqlImage.setObjectName("MysqlImage")
        self.MysqlImage.setScaledContents(True)
        self.MysqlImage.setGeometry(QtCore.QRect(widthL - (cdpi*(250/96))/2, heightL - ((((cdpi*(163/96))*1.5)/(w3/2)) + (self.uhost.frameGeometry().height()/2) + self.upass.frameGeometry().height() + self.uname.frameGeometry().height()), cdpi*(250/96), cdpi*(163/96)))


        widthE = self.Explorer.frameGeometry().width()
        heightE = self.Explorer.frameGeometry().height()
        
        
        self.ItemTreeView = QtWidgets.QTreeWidget(self.Explorer)
        self.ItemTreeView.setGeometry(QtCore.QRect(widthE/100 * 0.2, heightE/100 * 0.5, widthE/100 * 45, heightE/100 * 96.2))
        self.ItemTreeView.headerItem().setText(0, QtWidgets.QApplication.translate("MainWindow", "Database", None, -1))

        self.tableData = QtWidgets.QTableWidget(self.Explorer)
        self.tableData.setGeometry(QtCore.QRect(widthE/100 * 46, heightE/100 * 0.5, widthE/100 * 53.8, heightE/100 * 96.2))
        self.tableData.setObjectName("tableData")

        self.cdbWindow = QtWidgets.QWidget()
        self.cdbWindow.setObjectName("cdbWindow")
        self.cdbWindow.resize((300*cdpi)/(wpx/(cdpi/6)), (200*cdpi)/(hpx/(cdpi/10)))#7.9875*cdpi
        
        self.dbnameLabel = QtWidgets.QLabel(self.cdbWindow)
        self.dbnameLabel.setObjectName("dbnameLabel")
        self.dbnameLabel.setScaledContents(True)
        self.dbnameLabel.setGeometry(QtCore.QRect(self.cdbWindow.frameGeometry().width()/2 - ((165*wpx/(cdpi*11.25))/4), self.cdbWindow.frameGeometry().height()/2 - (50*hpx/(cdpi*11.25))*1.25, 165*wpx/(cdpi*11.25), 50*hpx/(cdpi*11.25)))
        
        self.dbname = QtWidgets.QLineEdit(self.cdbWindow)
        self.dbname.setObjectName("dbname")
        self.dbname.setPlaceholderText("New Database Name")
        self.dbname.setGeometry(QtCore.QRect(self.cdbWindow.frameGeometry().width()/2 - ((w/10.9714)/2), self.cdbWindow.frameGeometry().height()/2, w/10.9714, (cdpi/11) * w3))

        self.cdbButton = QtWidgets.QPushButton(self.cdbWindow)
        self.cdbButton.setObjectName("cdbButton")
        self.cdbButton.setGeometry(QtCore.QRect(self.cdbWindow.frameGeometry().width()/2 - ((w/10.9714)/2), self.cdbWindow.frameGeometry().height()/2 + ((cdpi/11) * w3)*1.5, w/10.9714, (cdpi/11) * w3))

        self.ctWindow = QtWidgets.QWidget()
        self.ctWindow.setObjectName("ctWindow")
        self.ctWindow.resize((450*cdpi)/(wpx/(cdpi/6)), (400*cdpi)/(hpx/(cdpi/8)))

        widthA = self.ctWindow.frameGeometry().width()
        heightA = self.ctWindow.frameGeometry().height()
        
        self.tname = QtWidgets.QLineEdit(self.ctWindow)
        self.tname.setObjectName("tname")
        self.tname.setPlaceholderText("New Table Name")
        self.tname.setGeometry(QtCore.QRect(widthA/2 - (w/10.9714/2), heightA/2, w/10.9714, (cdpi/11) * w3))

        self.addColumn = QtWidgets.QListWidget(self.ctWindow)
        self.addColumn.setGeometry(QtCore.QRect(widthE/100 * 0.2, heightE/100 * 0.5, widthE/100 * 20, heightE/100 * 96.2))
        self.addColumn.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.addColumn.setItemAlignment(QtCore.Qt.AlignLeading)
        self.addColumn.setObjectName("addColumn")
        self.addColumn.setContextMenuPolicy(Qt.CustomContextMenu)

        self.ateWindow = QtWidgets.QWidget()
        self.ctWindow.setObjectName("ctWindow")
        self.ctWindow.resize((250*cdpi)/(wpx/(cdpi/6)), (200*cdpi)/(hpx/(cdpi/8)))

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        self.mysqlExplorer.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        try:
            path = str(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))) + os.sep + 'MySQLExplorerData'
            os.mkdir(path)
        except FileExistsError:
            pass
        try:
            fblank = str(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))) + os.sep + 'MySQLExplorerData' + os.sep + '!=!SELECT-A-SAVE!=!.txt'
            wrbfile = open(fblank, 'w')
            wrbfile.write("")
            wrbfile.close()
        except FileExistsError:
            pass

        if not os.listdir(path):
            pass
        else:
            for file in os.listdir(path):
                if file.endswith('.txt'):
                    self.DropDown.addItem(file[0:len(file) - 4])

        def login():
            try:
                cnx = mysql.connector.connect(user=self.uname.text(), password=self.upass.text(), host=self.uhost.text(), port=self.uport.text())
                LoadTree()
            ##except mysql.connector.Error as err:
            ##    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            ##        messagebox.showerror("MySQL Login Error","Something is wrong with your username or password. Please try again.")
            ##        cnx.close()
            ##    else:
            ##        messagebox.showerror("MySQL Error",err)
            except mysql.connector.Error as e:
                if Error(errno=2003):
                    print("Error code:", e.errno)        # error number
                    print("SQLSTATE value:", e.sqlstate) # SQLSTATE value
                    print("Error message:", e.msg)          # error message
                    print("Error:", e)                  # errno, sqlstate, msg values
                    s = str(e)
                    print("Error:", s)                  # errno, sqlstate, msg values
                else:
                    print('AAAAAAAAA')
                    print("Error code:", e.errno)        # error number
                    print("SQLSTATE value:", e.sqlstate) # SQLSTATE value
                    print("Error message:", e.msg)          # error message
                    print("Error:", e)                  # errno, sqlstate, msg values
                    s = str(e)
                    print("Error:", s)                  # errno, sqlstate, msg values
            except (_mysql_connector.MySQLInterfaceError, mysql.connector.errors.DatabaseError):
                #exception to handle the user being unable to connect to the MySQL server
                print('E')
                #pass
            else:
                self.mysqlExplorer.setCurrentIndex(1)
                cnx.close()
        
        def savelogin():
            saveuser = str(self.uname.text())
            savepass = str(self.upass.text())
            savehost = str(self.uhost.text())
            saveport = str(self.uport.text())
            if saveuser == '' or saveport == '' or savehost == '':
                self.SaveLogin.setChecked(False)
            else:
                if os.path.isfile(path + os.sep + saveuser + '.txt') == False:
                    wrfile = open(os.path.join(path, str(saveuser) + '.txt'), 'w')
                    wrfile.write(saveuser + '\n' + savepass + '\n' + savehost + '\n' + saveport)
                    wrfile.close()
                else:
                    self.SaveLogin.setChecked(False)
                    messagebox.showerror("MySQL Explorer", "There is already saved data on the username " + saveuser + ''', so we will not be able to save your data while a save with your username exists!
Please Consider editing the data file, deleting the datafile, or using another account''')

        def loadsave():
            pick = str(self.DropDown.currentText())
            if pick == '!=!SELECT-A-SAVE!=!':
                pass
            else:
                path = path = str(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))) + os.sep + 'MySQLExplorerData' + os.sep
                unamedata = str(open(path + pick + '.txt', 'r').readlines()[0:1])
                upassdata = str(open(path + pick + '.txt', 'r').readlines()[1:2])
                uhostdata = str(open(path + pick + '.txt', 'r').readlines()[2:3])
                uportdata = str(open(path + pick + '.txt', 'r').readlines()[3:4])
                udlen = len(unamedata) - 4
                updlen = len(upassdata) - 4
                hdlen = len(uhostdata) - 4
                pdlen = len(uportdata) - 2
                self.uname.setText(unamedata[2:udlen])
                self.upass.setText(upassdata[2:updlen])
                self.uhost.setText(uhostdata[2:hdlen])
                self.uport.setText(uportdata[2:pdlen])

        def getItemParent():
            if self.ItemTreeView.indexOfTopLevelItem(self.ItemTreeView.currentItem()) == -1:
                return tuple((self.ItemTreeView.currentItem().parent().text(0), self.ItemTreeView.currentItem().text(0)))
            else:
                return None

##        def databaseContext(position):
##            c3n3xx = mysql.connector.connect(user=self.uname.text(), password=self.upass.text(), host=self.uhost.text(), port=self.uport.text())
##            cursor = c3n3xx.cursor()
##            menuD = QMenu()
##            createDB = menuD.addAction("Create Database")
##            deleteDB = menuD.addAction("Delete Database")
##            action = menuD.exec_(self.databaseView.mapToGlobal(position))
##            if action == deleteDB:
##                delete_item = self.databaseView.currentItem().text()
##                warnddatabase = QMessageBox()
##                popwarnddatabase = warnddatabase.warning(QtWidgets.QWidget(),'Deletion Confirmation', "Are you sure you would like to delete the database \"" + delete_item + "\"? All tables inside of the database will be lost!", warnddatabase.Yes, warnddatabase.No)
##                if popwarnddatabase == warnddatabase.Yes:
##                    cursor.execute("DROP DATABASE " + delete_item)
##                    LoadTree()
##                    c3n3xx.close()
##            if action == createDB:
##                self.cdbWindow.show()
##                LoadTree()
##                c3n3xx.close()
##            else:
##                c3n3xx.close()

        def tableContext(position):
            print('no')
##            try:
##                if getItemParent() != None:
##                    var = getItemParent()
##                else:
##                    raise Invalid
##                c3n3xx = mysql.connector.connect(user=self.uname.text(), password=self.upass.text(), host=self.uhost.text(), port=self.uport.text())
##                cursor = c3n3xx.cursor()
##                menuT = QMenu()
##                createT = menuT.addAction("Create Table")
##                deleteT = menuT.addAction("Delete Table")
##                action = menuT.exec_(self.ItemTreeView.viewport().mapToGlobal(position))
##                if action == deleteT:
##                    db_from = var[0]
##                    delete_item = var[1]
##                    warndtable = QMessageBox()
##                    popwarndtable = warndtable.warning(QtWidgets.QWidget(),'Deletion Confirmation', "Are you sure you would like to delete the table \"" + delete_item + "\"? All information inside of the table will be lost!", warndtable.Yes, warndtable.No)
##                    if popwarndtable == warndtable.Yes:
##                        cursor.execute("USE " + db_from)
##                        cursor.execute("DROP TABLE " + delete_item)
##                        LoadTree()
##                        c3n3xx.close()
##                    else:
##                        c3n3xx.close()
##                elif action == createT:
##                    self.ctWindow.show()
##                    LoadTree()
##                    c3n3xx.close()
##                else:
##                    c3n3xx.close()
##            except Invalid:
##                pass

        def LoadTree():
            cnnxx = mysql.connector.connect(user='root', password='200513314minecraftcocJV', host='127.0.0.1', port='3306')
            cursor = cnnxx.cursor()
            cursor.execute("SHOW DATABASES")
            dbases = cursor.fetchall()
            i = 0
            for item in dbases:
                itemID = str(item)[2:len(item)-4]
                Item64ID = QTreeWidgetItem(itemID)
                Item64ID.setText(0, itemID)
                try:
                    ccnnxx = mysql.connector.connect(user='root', password='200513314minecraftcocJV', host='127.0.0.1', port='3306', database=str(itemID))
                    cursor2 = ccnnxx.cursor()
                    cursor2.execute("SHOW TABLES")
                    tbls = cursor2.fetchall()
                    for table in tbls:
                        tblID = str(table)[2:len(table)-4]
                        tbl64ID = QTreeWidgetItem(tblID)
                        tbl64ID.setText(0, tblID)
                        Item64ID.addChild(tbl64ID)
                except mysql.connector.errors.InterfaceError:
                    pass
                    
                self.ItemTreeView.addTopLevelItem(Item64ID)
                i +=1

            cnnxx.close()

        def LoadTable():
            self.tableData.clear()

            try:
                if getItemParent() != None:
                    var = getItemParent()
                else:
                    raise Invalid
                ccnnxx = mysql.connector.connect(user=self.uname.text(), password=self.upass.text(), host=self.uhost.text(), port=self.uport.text(), database = var[0])
                cursor = ccnnxx.cursor()
                self.tableData.setRowCount(0)
                self.tableData.setColumnCount(0)
                header = self.tableData.horizontalHeader()       
                item = getItemParent()
                cursor.execute("SELECT * FROM " + var[1])
                rows = cursor.fetchall()
                self.tableData.setRowCount(cursor.rowcount)
                ccnnxx.close()
                self.tableData.setColumnCount(len(rows[0]))
                columnNames = [a[0] for a in cursor.description]
                g = 0
                h = 0
                i = 0
                j = 0
                k = 0
                a = 1
                counter = 0
                if a == 1:
                    for items in columnNames:
                        item = QtWidgets.QTableWidgetItem()
                        self.tableData.setHorizontalHeaderItem(g, item)
                        self.tableData.horizontalHeaderItem(g).setText(QtWidgets.QApplication.translate("MainWindow", columnNames[h], None, -1))
                        header.setSectionResizeMode(g, QtWidgets.QHeaderView.ResizeToContents)
                        g += 1
                        h += 1
                    for row in rows:
                        counter += 1
                        if i < counter:
                            while j != len(rows[0]):
                                item = QtWidgets.QTableWidgetItem()
                                self.tableData.setItem(i, k, item)
                                self.tableData.item(i, k).setText(QtWidgets.QApplication.translate("MainWindow", str(row[j]), None, -1))
                                k +=1
                                j +=1
                            else:
                                i +=1
                                k = 0
                                j = 0
                        else:
                            k = 0
                            j = 0
                    a = 2
                else:
                    pass
            except IndexError:
                #print('This table has no information!')
                pass
            except Invalid:
                #print('not a table')
                pass
                
                
        def editItem():
            rowid = self.tableData.currentRow()
            column = self.tableData.currentColumn()
            if column != -1 or rowid != -1:
                c4n3x3 = mysql.connector.connect(user=self.uname.text(), password=self.upass.text(), host=self.uhost.text(), port=self.uport.text(), database = self.databaseView.currentItem().text())
                cursor = c4n3x3.cursor()
                iteme = self.tableView.currentItem().text()
                cursor.execute("SELECT * FROM " + iteme)
                rows2 = cursor.fetchall()
                a = -1
                for row2 in rows2:
                    a += 1
                    if a == rowid:
                        #print(row2)
                        cc = len(rows2[0]) - column
                        itemc = len(rows2[0]) - cc
                        print(self.tableData.item(rowid, column).text())
                        print(row2[itemc])
                        LoadTable()
            else:
                pass

        def cdatabase():
            c3n3x3 = mysql.connector.connect(user=self.uname.text(), password=self.upass.text(), host=self.uhost.text(), port=self.uport.text(), database = self.databaseView.currentItem().text())
            cursor = c3n3x3.cursor()
            cdbnamevar = self.dbname.text()
            print(cdbnamevar)
            cursor.execute("CREATE DATABASE " + cdbnamevar)
            self.dbname.clear()
            self.cdbWindow.hide()
            c3n3x3.close()
            LoadTree()

        def ctable():
            pass
        
        def resizeUI():
            width = MainWindow.frameGeometry().width()
            height = MainWindow.frameGeometry().height()
            self.mysqlExplorer.setGeometry(QtCore.QRect(0, 0, width, height))
            widthL = self.mysqlExplorer.frameGeometry().width()/10 * 5
            heightL = self.mysqlExplorer.frameGeometry().height()/10 * 5
            w2 = cdpi/96
            w3 = hpx/432
            self.unameLabel.setGeometry(QtCore.QRect(widthL - self.unameLabel.width() * w2, heightL - (cdpi/11) * 6.5, self.unameLabel.width(), (cdpi/11) * w3))
            self.uname.setGeometry(QtCore.QRect(widthL - (self.unameLabel.frameGeometry().width() * 2.5)/6, heightL - (cdpi/11) * 6.5, self.unameLabel.frameGeometry().width() * (w2*2), (cdpi/11) * w3))
            self.upassLabel.setGeometry(QtCore.QRect(widthL - self.upassLabel.width() * w2, heightL - (cdpi/11) * 3.5, self.upassLabel.width(), (cdpi/11) * w3))
            self.upass.setGeometry(QtCore.QRect(widthL - (self.unameLabel.frameGeometry().width() * 2.5)/6, heightL - (cdpi/11) * 3.5, self.unameLabel.frameGeometry().width() * (w2*2), (cdpi/11) * w3))
            self.hostLabel.setGeometry(QtCore.QRect(widthL - self.hostLabel.width() * w2, heightL - (cdpi/11) * 0.5, self.hostLabel.width(), (cdpi/11) * w3))
            self.uhost.setGeometry(QtCore.QRect(widthL - (self.unameLabel.frameGeometry().width() * 2.5)/6, heightL - (cdpi/11) * 0.5, self.unameLabel.frameGeometry().width() * (w2*2), (cdpi/11) * w3))
            self.uportLabel.setGeometry(QtCore.QRect(widthL - self.uportLabel.width() * w2, heightL + (cdpi/11) * 2.5, self.uportLabel.width(), (cdpi/11) * w3))
            self.uport.setGeometry(QtCore.QRect(widthL - (self.unameLabel.frameGeometry().width() * 2.5)/6, heightL + (cdpi/11) * 2.5, self.unameLabel.frameGeometry().width() * (w2*2), (cdpi/11) * w3))
            self.DropDownLabel.setGeometry(QtCore.QRect(widthL - self.DropDownLabel.width() * w2, heightL + (cdpi/2), self.DropDownLabel.width() + 2, (cdpi/11) * w3))
            self.DropDown.setGeometry(QtCore.QRect(widthL - (self.unameLabel.frameGeometry().width() * 2.5)/6, heightL + (cdpi/2), self.unameLabel.frameGeometry().width() * (w2*2), (cdpi/11) * w3))
            self.SaveLogin.setGeometry(QtCore.QRect(widthL -  110* w2, heightL + (cdpi/11) * 9, 120, (cdpi/11) * (w3/1.66)))
            self.LoginButton.setGeometry(QtCore.QRect(widthL - (self.unameLabel.frameGeometry().width() * 2.5)/6, heightL + (cdpi/11) * 8.5, self.unameLabel.frameGeometry().width() * (w2*2), (cdpi/11) * w3))
            self.LoginButton.setGeometry(QtCore.QRect(widthL - (self.unameLabel.frameGeometry().width() * 2.5)/6, heightL + (cdpi/11) * 8.5, self.unameLabel.frameGeometry().width() * (w2*2), (cdpi/11) * w3))
            self.MysqlImage.setGeometry(QtCore.QRect(widthL - (cdpi*(250/96))/2, heightL - ((((cdpi*(163/96))*1.5)/(w3/2)) + (self.uhost.frameGeometry().height()/2) + self.upass.frameGeometry().height() + self.uname.frameGeometry().height()), cdpi*(250/96), cdpi*(163/96)))
            widthE = self.mysqlExplorer.frameGeometry().width()/cdpi
            heightE = self.mysqlExplorer.frameGeometry().height()/cdpi
            self.ItemTreeView.setGeometry(QtCore.QRect(widthE*0.2, heightE - (cdpi*(2/96)), 3.8*cdpi, (heightE*cdpi - (cdpi*(53.5/96)))))
            self.tableData.setGeometry(QtCore.QRect(cdpi*(5/96)+(self.ItemTreeView.frameGeometry().width()), heightE - (cdpi*(2/96)), (widthE*cdpi - self.ItemTreeView.frameGeometry().width()) - widthE*1.4, (heightE*cdpi - (cdpi*(53.5/96)))  ))

        self.DropDown.activated.connect(loadsave)
        self.LoginButton.clicked.connect(login)
        self.SaveLogin.clicked.connect(savelogin)
        self.cdbButton.clicked.connect(cdatabase)
        self.tableData.itemChanged.connect(editItem)
        self.ItemTreeView.customContextMenuRequested.connect(tableContext)
        self.ItemTreeView.itemActivated.connect(LoadTable)
        MainWindow.resized.connect(resizeUI)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MySQL Explorer", None, -1))
        self.cdbWindow.setWindowTitle(QtWidgets.QApplication.translate("cdbWindow", "DB Create", None, -1))
        self.DropDownLabel.setText(QtWidgets.QApplication.translate("MainWindow", "Saved Logins", None, -1))
        self.unameLabel.setText(QtWidgets.QApplication.translate("MainWindow", "Username", None, -1))
        self.upassLabel.setText(QtWidgets.QApplication.translate("MainWindow", "Password", None, -1))
        self.hostLabel.setText(QtWidgets.QApplication.translate("MainWindow", "Host", None, -1))
        self.uportLabel.setText(QtWidgets.QApplication.translate("MainWindow", "Port", None, -1))
        self.SaveLogin.setText(QtWidgets.QApplication.translate("MainWindow", "Save Login", None, -1))
        self.LoginButton.setText(QtWidgets.QApplication.translate("MainWindow", "Login", None, -1))
        self.dbnameLabel.setText(QtWidgets.QApplication.translate("cdbWindow", "Please Enter the name of the\nnew database you would like\nto create!", None, -1))
        self.cdbButton.setText(QtWidgets.QApplication.translate("cdbWindow", "Create Database", None, -1))

class Window(QtWidgets.QMainWindow):
    resized = QtCore.Signal()
    def  __init__(self, parent=None):
        super(Window, self).__init__(parent=parent)
        ui = Ui_MainWindow()
        ui.setupUi(self)

    def resizeEvent(self, event):
        self.resized.emit()
        return super(Window, self).resizeEvent(event)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())

