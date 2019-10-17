from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import sys
from sys import platform
import os
import mysql.connector
from mysql.connector import errorcode
import tkinter as tk

root = tk.Tk()
wpx = root.winfo_screenwidth()
hpx = root.winfo_screenheight()

if platform == 'win32':
    import ctypes
    userwin = ctypes.windll.user32
    userwin.SetProcessDPIAware()
    [w, h] = [userwin.GetSystemMetrics(0), userwin.GetSystemMetrics(1)]
    cdpi = w*96/wpx
    myappid = 'mycompany.myproduct.subproduct.version'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
elif platform == 'darwin':
    from AppKit import NSScreen
    from Foundation import NSBundle
    h = NSScreen.mainScreen().frame().size.height
    w = NSScreen.mainScreen().frame().size.width
    cdpi = w*96/wpx
    bundle = NSBundle.mainBundle()
    if bundle:
        info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
        if info and info['CFBundleName'] == 'Python':
            info['CFBundleName'] = 'MySQL Explorer'
#elif platform == 'linux1' or platform == 'linux2':


root.withdraw()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        
        # --- MAIN WINDOW ---
        
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

        # --- MYSQL LOGIN PAGE ---
        
        self.unameLabel = QtWidgets.QLabel(self.LoginPage)
        self.unameLabel.setObjectName("unameLabel")
        self.unameLabel.setScaledContents(True)

        self.uname = QtWidgets.QLineEdit(self.LoginPage)
        self.uname.setObjectName("uname")
        self.uname.setPlaceholderText("Username")
        
        self.upassLabel = QtWidgets.QLabel(self.LoginPage)
        self.upassLabel.setObjectName("upassLabel")
        self.upassLabel.setScaledContents(True)
             
        self.upass = QtWidgets.QLineEdit(self.LoginPage)
        self.upass.setObjectName("upass")
        self.upass.setPlaceholderText("Password")
        self.upass.setEchoMode(self.upass.Password)
        
        self.hostLabel = QtWidgets.QLabel(self.LoginPage)
        self.hostLabel.setObjectName("hostLabel")
        self.hostLabel.setScaledContents(True)
        
        self.uhost = QtWidgets.QLineEdit(self.LoginPage)
        self.uhost.setObjectName("uhost")
        self.uhost.setPlaceholderText("Local Host is 127.0.0.1")
        
        self.uportLabel = QtWidgets.QLabel(self.LoginPage)
        self.uportLabel.setObjectName("uportLabel")
        self.uportLabel.setScaledContents(True)
        
        self.uport = QtWidgets.QLineEdit(self.LoginPage)
        self.uport.setObjectName("uport")
        self.uport.setPlaceholderText("Default Port is 3306")

        self.DropDownLabel = QtWidgets.QLabel(self.LoginPage)
        self.DropDownLabel.setObjectName("DropDownLabel")
        self.DropDownLabel.setScaledContents(True)

        self.DropDown = QtWidgets.QComboBox(self.LoginPage)
        self.DropDown.setObjectName("DropDown")
        
        self.SaveLogin = QtWidgets.QCheckBox(self.LoginPage)
        self.SaveLogin.setObjectName("SaveLogin")
        
        self.LoginButton = QtWidgets.QPushButton(self.LoginPage)
        self.LoginButton.setObjectName("LoginButton")
        self.LoginButton.setAutoDefault(True)

        self.MysqlImage = QtWidgets.QLabel(self.LoginPage)
        self.MysqlImage.setText("")
        self.MysqlImage.setPixmap(QtGui.QPixmap("Login_Image.png"))
        self.MysqlImage.setObjectName("MysqlImage")
        self.MysqlImage.setScaledContents(True)

        # --- MYSQL EXPLORER ---

        self.databaseView = QtWidgets.QListWidget(self.Explorer)
        self.databaseView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        heightTD = self.databaseView.frameGeometry().height()
        self.databaseView.setItemAlignment(QtCore.Qt.AlignLeading)
        self.databaseView.setObjectName("databaseView")
        self.databaseView.setContextMenuPolicy(Qt.CustomContextMenu)

        self.tableView = QtWidgets.QListWidget(self.Explorer)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        heightTT = self.tableView.frameGeometry().height()
        self.tableView.setItemAlignment(QtCore.Qt.AlignLeading)
        self.tableView.setObjectName("tableView")
        self.tableView.setContextMenuPolicy(Qt.CustomContextMenu)

        self.tableData = QtWidgets.QTableWidget(self.Explorer)
        self.tableData.setObjectName("tableData")

        # --- DATABASE CREATOR ---
        w3 = hpx/432

        self.cdbWindow = QtWidgets.QWidget()
        self.cdbWindow.setObjectName("cdbWindow")
        self.cdbWindow.resize(cdpi*(200/96), cdpi*(130/96))

        widthB = self.cdbWindow.frameGeometry().width()
        heightB = self.cdbWindow.frameGeometry().height()
        
        self.dbnameLabel = QtWidgets.QTextBrowser(self.cdbWindow)
        self.dbnameLabel.setObjectName("dbnameLabel")
        self.dbnameLabel.setGeometry(QtCore.QRect((7/96)*cdpi, (7/96)*cdpi, cdpi*(187/96), cdpi*(60/96)))
        
        self.dbname = QtWidgets.QLineEdit(self.cdbWindow)
        self.dbname.setObjectName("dbname")
        self.dbname.setPlaceholderText("New Database Name")
        self.dbname.setGeometry(QtCore.QRect((7/96)*cdpi, self.cdbWindow.frameGeometry().height() - ((((cdpi/11) * w3)*1.5)*1.8), cdpi*(187/96), (cdpi/11) * w3))


        self.cdbButton = QtWidgets.QPushButton(self.cdbWindow)
        self.cdbButton.setObjectName("cdbButton")
        self.cdbButton.setGeometry(QtCore.QRect(self.cdbWindow.frameGeometry().width()/2 - ((w/10.9714)/2), self.cdbWindow.frameGeometry().height() - ((cdpi/11) * w3)*1.5, w/10.9714, (cdpi/10) * w3))

        # --- TABLE CREATOR ---

        self.ctWindow = QtWidgets.QWidget()
        self.ctWindow.setObjectName("ctWindow")
        self.ctWindow.resize((cdpi*(585/96)), (cdpi*(515/96)))
        self.ctWindow.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ctWindow.setMinimumSize((cdpi*(585/96)), (cdpi*(515/96)))
        self.ctWindow.setMaximumSize((cdpi*(585/96)), (cdpi*(515/96)))

        widthA = self.ctWindow.frameGeometry().width()
        heightA = self.ctWindow.frameGeometry().height()

        self.createtble = QtWidgets.QPushButton(self.ctWindow)
        self.createtble.setObjectName("createtble")
        self.createtble.setGeometry(QtCore.QRect((cdpi*(300/96)), (cdpi*(7/96)), (cdpi*(130/96)), (cdpi*(25/96))))

        self.tname = QtWidgets.QLineEdit(self.ctWindow)
        self.tname.setObjectName("tname")
        self.tname.setPlaceholderText(" Table Name")
        self.tname.setGeometry(QtCore.QRect((cdpi*(445/96)), (cdpi*(7/96)), (cdpi*(130/96)), (cdpi*(25/96))))

        self.addrow = QtWidgets.QPushButton(self.ctWindow)
        self.addrow.setObjectName("addrow")
        self.addrow.setGeometry(QtCore.QRect((cdpi*(10/96)), (cdpi*(7/96)), (cdpi*(130/96)), (cdpi*(25/96))))

        self.removerow = QtWidgets.QPushButton(self.ctWindow)
        self.removerow.setObjectName("removetble")
        self.removerow.setGeometry(QtCore.QRect((cdpi*(155/96)), (cdpi*(7/96)), (cdpi*(130/96)), (cdpi*(25/96))))

        self.rname = QtWidgets.QLineEdit(self.ctWindow)
        self.rname.setObjectName("tname")
        self.rname.setPlaceholderText(" New Row Name")
        self.rname.setGeometry(QtCore.QRect((cdpi*(10/96)), (cdpi*(70/96)), (cdpi*(275/96)), (cdpi*(25/96))))

        self.ctRows = QtWidgets.QTableWidget(self.ctWindow)
        self.ctRows.setGeometry(QtCore.QRect((cdpi*(10/96)), (cdpi*(100/96)), (cdpi*(275/96)), (cdpi*(405/96))))
        self.ctRows.setObjectName("ctRows")

        self.addcolumn = QtWidgets.QPushButton(self.ctWindow)
        self.addcolumn.setObjectName("addcolumn")
        self.addcolumn.setGeometry(QtCore.QRect((cdpi*(300/96)), (cdpi*(40/96)), (cdpi*(130/96)), (cdpi*(25/96))))

        self.removecolumn = QtWidgets.QPushButton(self.ctWindow)
        self.removecolumn.setObjectName("removecolumn")
        self.removecolumn.setGeometry(QtCore.QRect((cdpi*(445/96)), (cdpi*(40/96)), (cdpi*(130/96)), (cdpi*(25/96))))

        self.cname = QtWidgets.QLineEdit(self.ctWindow)
        self.cname.setObjectName("cname")
        self.cname.setPlaceholderText(" New Column Name")
        self.cname.setGeometry(QtCore.QRect((cdpi*(300/96)), (cdpi*(70/96)), (cdpi*(275/96)), (cdpi*(25/96))))

        self.ctColumns = QtWidgets.QListWidget(self.ctWindow)
        self.ctColumns.setGeometry(QtCore.QRect((cdpi*(300/96)), (cdpi*(100/96)), (cdpi*(275/96)), (cdpi*(405/96))))

        self.ctCPicker = QtWidgets.QComboBox(self.ctWindow)
        self.ctCPicker.setObjectName("ctCPicker")
        self.ctCPicker.setGeometry(QtCore.QRect((cdpi*(155/96)), (cdpi*(40/96)), (cdpi*(130/96)), (cdpi*(25/96))))
        #self.ctCPicker.addItem("Column")

        self.ctRPicker = QtWidgets.QComboBox(self.ctWindow)
        self.ctRPicker.setObjectName("ctRPicker")
        self.ctRPicker.setGeometry(QtCore.QRect((cdpi*(10/96)), (cdpi*(40/96)), (cdpi*(130/96)), (cdpi*(25/96))))
        self.ctRPicker.addItem("New Row")

        #self.ctWindow.show()

        # --- SETTING UP CONNECTIONS ---

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        self.mysqlExplorer.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # --- MAIN CODE ---

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
                ListDatabases()
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    messagebox.showerror("MySQL Login Error","Something is wrong with your user name or password. Please try again.")
                    cnx.close()
                else:
                    messagebox.showerror("MySQL Error",err)
                    cnx.close()
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
                path = str(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))) + os.sep + 'MySQLExplorerData' + os.sep
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

        def databaseContext(position):
            c3n3xx = mysql.connector.connect(user=self.uname.text(), password=self.upass.text(), host=self.uhost.text(), port=self.uport.text())
            cursor = c3n3xx.cursor()
            menuD = QMenu()
            createDB = menuD.addAction("Create Database")
            deleteDB = menuD.addAction("Delete Database")
            action = menuD.exec_(self.databaseView.mapToGlobal(position))
            if action == deleteDB:
                delete_item = self.databaseView.currentItem().text()
                warnddatabase = QMessageBox()
                popwarnddatabase = warnddatabase.warning(QtWidgets.QWidget(),'Deletion Confirmation', "Are you sure you would like to delete the database \"" + delete_item + "\"? All tables inside of the database will be lost!", warnddatabase.Yes, warnddatabase.No)
                if popwarnddatabase == warnddatabase.Yes:
                    cursor.execute("DROP DATABASE " + delete_item)
                    ListDatabases()
                    c3n3xx.close()
            if action == createDB:
                self.cdbWindow.show()
                ListDataBases()
                c3n3xx.close()
            else:
                c3n3xx.close()
                
        def tableContext(position):
            c3n3xx = mysql.connector.connect(user=self.uname.text(), password=self.upass.text(), host=self.uhost.text(), port=self.uport.text())
            cursor = c3n3xx.cursor()
            menuT = QMenu()
            createT = menuT.addAction("Create Table")
            deleteT = menuT.addAction("Delete Table")
            action = menuT.exec_(self.tableView.mapToGlobal(position))
            if action == deleteT:
                db_from = self.databaseView.currentItem().text()
                delete_item = self.tableView.currentItem().text()
                warndtable = QMessageBox()
                popwarndtable = warndtable.warning(QtWidgets.QWidget(),'Deletion Confirmation', "Are you sure you would like to delete the table \"" + delete_item + "\"? All information inside of the table will be lost!", warndtable.Yes, warndtable.No)
                if popwarndtable == warndtable.Yes:
                    cursor.execute("USE " + db_from)
                    cursor.execute("DROP TABLE " + delete_item)
                    ListTables()
                    c3n3xx.close()
                else:
                    c3n3xx.close()
            if action == createT:
                self.ctWindow.show()
                c3n3xx.close()
            else:
                c3n3xx.close()

        def ctbleContext(position):
            menucT = QMenu()
            cthelp = menucT.addAction("Help")
            action = menucT.exec_(self.ctWindow.mapToGlobal(position))
            if action == cthelp:
                pass

        def ListDatabases():
            self.tableView.clear()
            self.tableData.clear()
            cnnxx = mysql.connector.connect(user=self.uname.text(), password=self.upass.text(), host=self.uhost.text(), port=self.uport.text())
            cursor = cnnxx.cursor()
            databases = ("SHOW DATABASES")
            cursor.execute("SHOW DATABASES")
            dbases = cursor.fetchall()
            self.databaseView.clear()
            self.tableView.clear()
            self.tableData.clear()
            j = 0
            for item in dbases:
                self.databaseView.sizeHintForRow(j)
                self.databaseView.addItems(item)
                j +=1
            cnnxx.close()

        def ListTables():
            print(self.tableView.currentItem())
            self.tableView.setItemSelected(self.tableView.currentItem(), False)
            self.tableView.clear()
            self.tableData.clear()
            cnxx = mysql.connector.connect(user=self.uname.text(), password=self.upass.text(), host=self.uhost.text(), port=self.uport.text())
            cursor = cnxx.cursor()
            item = self.databaseView.currentItem().text()
            self.tableData.setRowCount(0)
            self.tableData.setColumnCount(0)
            cursor.execute("USE " + item)
            cursor.execute("SHOW TABLES")
            ddbases = cursor.fetchall()
            e = 0
            for item in ddbases:
                self.tableView.sizeHintForRow(e)
                self.tableView.addItems(item)
                e += 1
            cnxx.close()

        def LoadTable():
            self.tableData.clear()
            try:
                ccnnxx = mysql.connector.connect(user=self.uname.text(), password=self.upass.text(), host=self.uhost.text(), port=self.uport.text(), database = self.databaseView.currentItem().text())
                cursor = ccnnxx.cursor()
                self.tableData.setRowCount(0)
                self.tableData.setColumnCount(0)
                header = self.tableData.horizontalHeader()
                cursor.execute("SELECT * FROM " + self.tableView.currentItem().text())
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
                counter = 0
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
            except IndexError:
                #print('This table has no information!')
                pass
            except TypeError:
                pass
            except mysql.connector.errors.ProgrammingError:
                pass
                
                
        def editItem():
            rowid = self.tableData.currentRow()
            rowval = rowid.text()
            column = self.tableData.currentColumn()
            if column != -1 or rowid != -1:
                c4n3x3 = mysql.connector.connect(user=self.uname.text(), password=self.upass.text(), host=self.uhost.text(), port=self.uport.text(), database = self.databaseView.currentItem().text())
                cursor = c4n3x3.cursor()
                iteme = self.tableView.currentItem().text()
                cursor.execute("SELECT * FROM " + iteme)
                rows2 = cursor.fetchall()
                a = -1
                cursor.execute("UPDATE " + self.tableView.currentItem().text() + " SET " + column.text() + " = " + iteme + "WHERE " + column.text() + " = " + rowval)
                #for row2 in rows2:
                #    a += 1
                #    if a == rowid:
                #        #print(row2)
                #        cc = len(rows2[0]) - column
                #        itemc = len(rows2[0]) - cc
                #        print(self.tableData.item(rowid, column).text())
                #        print(row2[itemc])
                #        LoadTable()
            else:
                pass

        def cdatabase():
            c3n3x3 = mysql.connector.connect(user=self.uname.text(), password=self.upass.text(), host=self.uhost.text(), port=self.uport.text())
            cursor = c3n3x3.cursor()
            cursor.execute("CREATE DATABASE " + self.dbname.text())
            self.dbname.clear()
            self.cdbWindow.hide()
            c3n3x3.close()
            ListDatabases()

        def ctable():
            colnames = []
            rvals = []
            vals = []
            allRows = self.ctRows.rowCount()
            allColumns = self.ctRows.columnCount()
            for rows in range(allRows):
                for columns in range(allColumns):
                    if self.ctRows.item(rows, columns).text() != "":
                        u = self.ctRows.item(rows, columns).text()
                    else:
                        u = ""
                    rvals.append(u)
                vals.append(tuple(rvals))
                rvals = []
            a = 0
            for y in range(self.ctColumns.count()):
                colnames.append(self.ctColumns.item(y).text())
                a += 1
            if a == 1:
                tcoln = '('+str([c for c in colnames])[1:len([c for c in colnames])-2]+')'
            else:
                tcoln = tuple(colnames)
            if self.tname.text() != "":
                sql = "CREATE TABLE "+self.tname.text()+" "+str(tcoln)+" VALUES "+str(vals)
                c4n4x5 = mysql.connector.connect(user=self.uname.text(), password=self.upass.text(), host=self.uhost.text(), port=self.uport.text(), database = self.databaseView.currentItem().text())
                cursor = c4n4x5.cursor()
                cursor.execute(sql)
                self.ctWindow.hide()
                ListDatabases()
            else:
                print("YOU TABLE NEEDS A NAME")
            

        def ctaddrow():
            if self.ctRPicker.currentText() == "New Row":
                g = self.ctRows.rowCount()
                self.ctRPicker.addItem(str(self.ctRPicker.count()))
            else:
                g = int(self.ctRPicker.currentText()) - 1

            if self.ctCPicker.currentText() == "":
                h = 0
            else:
                h = self.ctCPicker.currentIndex()

            item = QtWidgets.QTableWidgetItem(self.rname.text())
            self.ctRows.setRowCount(g+1)
            self.ctRows.setItem(g, h, item)

        def ctaddcolumn():
            columnName = self.cname.text()
            self.ctCPicker.addItem(columnName)
            self.ctColumns.addItem(columnName)
            g = self.ctRows.columnCount()
            item = QtWidgets.QTableWidgetItem(columnName)
            self.ctRows.setColumnCount(g+1)
            self.ctRows.setHorizontalHeaderItem(g, item) 

        def ctremoverow():
            self.ctRows.removeRow(self.ctRows.row(self.ctRows.currentItem()))

        def ctremovecolumn():
            self.ctColumns.takeItem(self.ctColumns.row(self.ctColumns.currentItem()))
            print("ListView: "+str(self.ctColumns.row(self.ctColumns.currentItem())))
            self.ctRows.removeColumn(self.ctColumns.row(self.ctColumns.currentItem()))
            print("TableWidget: "+str(self.ctRows.columnCount()))
            print(" ")

        # --- HANDLE WINDOW RESIZES ---
        
        def resizeUI():
            width = MainWindow.frameGeometry().width()
            height = MainWindow.frameGeometry().height()
            self.mysqlExplorer.setGeometry(QtCore.QRect(0, 0, width, height))
            widthL = self.mysqlExplorer.frameGeometry().width()/2
            heightL = self.mysqlExplorer.frameGeometry().height()/2
            w2 = cdpi/80
            w3 = hpx/432
            self.unameLabel.setGeometry(QtCore.QRect(widthL - self.unameLabel.width() * w2, heightL - (cdpi/11) * 6.5, self.unameLabel.width(), (cdpi/11) * w3))
            self.uname.setGeometry(QtCore.QRect(widthL - (self.unameLabel.frameGeometry().width() * 2.5)/6, heightL - (cdpi/11) * 6.5, self.unameLabel.frameGeometry().width() * (w2*2), (cdpi/11) * w3))
            self.upassLabel.setGeometry(QtCore.QRect(widthL - self.upassLabel.width() * w2, heightL - (cdpi/11) * 3.5, self.upassLabel.width(), (cdpi/11) * w3))
            self.upass.setGeometry(QtCore.QRect(widthL - (self.unameLabel.frameGeometry().width() * 2.5)/6, heightL - (cdpi/11) * 3.5, self.unameLabel.frameGeometry().width() * (w2*2), (cdpi/11) * w3))
            self.hostLabel.setGeometry(QtCore.QRect(widthL - self.hostLabel.width() * w2, heightL - (cdpi/11) * 0.5, self.hostLabel.width(), (cdpi/11) * w3))
            self.uhost.setGeometry(QtCore.QRect(widthL - (self.unameLabel.frameGeometry().width() * 2.5)/6, heightL - (cdpi/11) * 0.5, self.unameLabel.frameGeometry().width() * (w2*2), (cdpi/11) * w3))
            self.uportLabel.setGeometry(QtCore.QRect(widthL - self.uportLabel.width() * w2, heightL + (cdpi/11) * 2.5, self.uportLabel.width(), (cdpi/11) * w3))
            self.uport.setGeometry(QtCore.QRect(widthL - (self.unameLabel.frameGeometry().width() * 2.5)/6, heightL + (cdpi/11) * 2.5, self.unameLabel.frameGeometry().width() * (w2*2), (cdpi/11) * w3))
            self.DropDownLabel.setGeometry(QtCore.QRect(widthL - (self.unameLabel.frameGeometry().width() * (w2)), heightL + (cdpi/2), (100/96)*cdpi, (cdpi/11) * w3))
            self.DropDown.setGeometry(QtCore.QRect(widthL - (self.unameLabel.frameGeometry().width() * 2.5)/6, heightL + (cdpi/2), self.unameLabel.frameGeometry().width() * (w2*2), (cdpi/11) * w3))
            self.SaveLogin.setGeometry(QtCore.QRect(widthL -  110* w2, heightL + (cdpi/11) * 9, 120, (cdpi/11) * (w3/1.66)))
            self.LoginButton.setGeometry(QtCore.QRect(widthL - (self.unameLabel.frameGeometry().width() * 2.5)/6, heightL + (cdpi/11) * 8.5, self.unameLabel.frameGeometry().width() * (w2*2), (cdpi/11) * w3))
            self.LoginButton.setGeometry(QtCore.QRect(widthL - (self.unameLabel.frameGeometry().width() * 2.5)/6, heightL + (cdpi/11) * 8.5, self.unameLabel.frameGeometry().width() * (w2*2), (cdpi/11) * w3))
            self.MysqlImage.setGeometry(QtCore.QRect(widthL - (cdpi*(250/96))/2, heightL - ((((cdpi*(163/96))*1.5)/(w3/2)) + (self.uhost.frameGeometry().height()/2) + self.upass.frameGeometry().height() + self.uname.frameGeometry().height()), cdpi*(250/96), cdpi*(163/96)))
            widthE = self.mysqlExplorer.frameGeometry().width()
            heightE = self.mysqlExplorer.frameGeometry().height()
            self.databaseView.setGeometry(QtCore.QRect(widthE/100 * 0.2, heightE/100 * 0.5, widthE/100 * 20, (heightE/100 * 95) - 10))
            self.tableView.setGeometry(QtCore.QRect(widthE/100 * 20.4, heightE/100 * 0.5, widthE/100 * 25, (heightE/100 * 95) - 10))
            self.tableData.setGeometry(QtCore.QRect(widthE/100 * 45.7, heightE/100 * 0.5, widthE/100 * 53.9, (heightE/100 * 95) - 10))

        # --- BUTTON CONNECTIONS ---
            
            # --- LOGIN PAGE ---
        self.LoginButton.clicked.connect(login)
        self.SaveLogin.clicked.connect(savelogin)
        self.DropDown.activated.connect(loadsave)
            # --- EXPLORER PAGE ---
        self.databaseView.itemSelectionChanged.connect(ListTables)
        self.tableView.itemSelectionChanged.connect(LoadTable)
        self.databaseView.customContextMenuRequested.connect(databaseContext)
        self.tableView.customContextMenuRequested.connect(tableContext)
        self.tableData.itemChanged.connect(editItem)
            # --- DATABASE CREATION PAGE ---
        self.cdbButton.clicked.connect(cdatabase)
            # --- TABLE CREATION PAGE ---
        self.ctWindow.customContextMenuRequested.connect(ctbleContext)
        self.addrow.clicked.connect(ctaddrow)
        self.removerow.clicked.connect(ctremoverow)
        self.addcolumn.clicked.connect(ctaddcolumn)
        self.removecolumn.clicked.connect(ctremovecolumn)
        self.createtble.clicked.connect(ctable)
            # --- MAIN WINDOW RESIZE DETECTION ---
        MainWindow.resized.connect(resizeUI)

    # --- SETTING OBJECT NAMES ---

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MySQL Explorer", None, -1))
        self.DropDownLabel.setText(QtWidgets.QApplication.translate("MainWindow", "Saved Logins", None, -1))
        self.unameLabel.setText(QtWidgets.QApplication.translate("MainWindow", "Username", None, -1))
        self.upassLabel.setText(QtWidgets.QApplication.translate("MainWindow", "Password", None, -1))
        self.hostLabel.setText(QtWidgets.QApplication.translate("MainWindow", "Host", None, -1))
        self.uportLabel.setText(QtWidgets.QApplication.translate("MainWindow", "Port", None, -1))
        self.SaveLogin.setText(QtWidgets.QApplication.translate("MainWindow", "Save Login", None, -1))
        self.LoginButton.setText(QtWidgets.QApplication.translate("MainWindow", "Login", None, -1))
        # --- Database Creator ---
        self.cdbWindow.setWindowTitle(QtWidgets.QApplication.translate("cdbWindow", "Database Creator", None, -1))
        self.dbnameLabel.setText(QtWidgets.QApplication.translate("cdbWindow", "Please Enter the name of the new database you would like to create. Then hit the \"create database\" button to create the new database!", None, -1))
        self.cdbButton.setText(QtWidgets.QApplication.translate("cdbWindow", "Create Database", None, -1))
        # --- Table Creator ---
        self.ctWindow.setWindowTitle(QtWidgets.QApplication.translate("ctWindow", 'Table Creator'))
        self.createtble.setText(QtWidgets.QApplication.translate("ctWindow", "Create Table"))
        self.addrow.setText(QtWidgets.QApplication.translate("ctWindow", "+ Add Row"))
        self.removerow.setText(QtWidgets.QApplication.translate("ctWindow", "- Remove Row"))
        self.addcolumn.setText(QtWidgets.QApplication.translate("ctWindow", "+ Add Column"))
        self.removecolumn.setText(QtWidgets.QApplication.translate("ctWindow", "- Remove Column"))

# --- CREATING WINDOW RESIZED SIGNAL ---

class Window(QtWidgets.QMainWindow):
    resized = QtCore.Signal()
    def  __init__(self, parent=None):
        super(Window, self).__init__(parent=parent)
        ui = Ui_MainWindow()
        ui.setupUi(self)

    def resizeEvent(self, event):
        self.resized.emit()
        return super(Window, self).resizeEvent(event)

# --- STARTUP ---

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('Window_Icon.png'))
    #Showing Window Class instead of the Ui_MainWindow Class
    #Because the Ui_MainWindow is "Projected" through the Window Class
    #There for allowing it to detect resizes (Not 100% sure since im not an expert and its code i modified to fit my needs)
    w = Window()
    w.show()
    sys.exit(app.exec_())

