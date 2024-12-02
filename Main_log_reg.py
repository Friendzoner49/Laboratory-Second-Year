from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi
from PyQt6.QtGui import QShortcut, QIcon
from PyQt6.QtCore import Qt
import sys, os
import sqlite3 as mdb


def resource_path(relative_path):
    """Trả về đường dẫn tài nguyên, hỗ trợ khi đóng gói."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def custom_boxmessagemini(parent, title, text, icon_path):
    msg = QMessageBox(parent)
    msg.setWindowIcon(QIcon(resource_path(icon_path)))  # Đặt icon từ file
    msg.setWindowTitle(title)  # Đặt tiêu đề
    msg.setText(text)  # Đặt nội dung
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)  # Nút "Ok"

    msg.setStyleSheet(f"QLabel{{min-width: {140 - 50}px; min-height: {70 - 50}px;}}")
    msg.resize(400, 200)
    
    msg.exec()

def custom_boxmessagebig(parent, title, text, icon_path):
    msg = QMessageBox(parent)
    msg.setWindowIcon(QIcon(resource_path(icon_path)))  # Đặt icon từ file
    msg.setWindowTitle(title)  # Đặt tiêu đề
    msg.setText(text)  # Đặt nội dung
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)  # Nút "Ok"

    msg.setStyleSheet(f"QLabel{{min-width: {300 - 50}px; min-height: {70 - 50}px;}}")
    msg.resize(400, 200)
    
    msg.exec()

#Login
class Login_w(QMainWindow):
    def __init__(self):
        super(Login_w, self).__init__()
        uic.loadUi('Login.ui', self)
        self.login_bt.clicked.connect(self.login)
        self.regis_bt.clicked.connect(self.reg_form)
        
        self.enter_shortcut = QShortcut(QtCore.Qt.Key.Key_Return, self)
        self.enter_shortcut.activated.connect(self.login)
    def reg_form(self):
        widget.setCurrentIndex(1)

    def showEvent(self, event):
        super().showEvent(event)
        # Đặt focus vào trường đầu tiên (user_log)
        self.user_log.setFocus()

    def login(self):
        unl = self.user_log.text()
        pswl = self.pass_log.text()
        db = mdb.connect('1.db')
        query = db.cursor()
        query.execute("select * from user_list where user= '"+unl+"' and pass= '"+pswl+"' ")
        kt = query.fetchone()
        if kt:
            custom_boxmessagemini(self, "Login output", "Login success", "icons/home-icon.png")
            widget.setCurrentIndex(2)
        else:
            QMessageBox.warning(self, "Login output", "Login failed")

#Register
class Reg_w(QMainWindow):
    def __init__(self):
        super(Reg_w, self).__init__()
        uic.loadUi('Register.ui', self)
        self.regisnew_bt.clicked.connect(self.reg)

        self.enter_shortcut = QShortcut(QtCore.Qt.Key.Key_Return, self)
        self.enter_shortcut.activated.connect(self.reg)

    def showEvent(self, event):
        super().showEvent(event)
        # Đặt focus vào trường đầu tiên (user_log)
        self.user_reg.setFocus()

    def reg(self):
        un = self.user_reg.text()
        psw = self.pass_reg.text()
        db = mdb.connect('1.db')
        query = db.cursor()
        query.execute("select * from user_list where user='"+un+"' ")
        kt = query.fetchone()
        if kt:
            
            QMessageBox.warning(self, "Register output", "User already exists")
            widget.setCurrentIndex(1)
        else:
            query.execute("insert into user_list values ('"+un+"','"+psw+"') ")
            db.commit()
            custom_boxmessagemini(self, "Register output", "Register Success", "icons/register.png")
            widget.setCurrentIndex(0)

#Menu
class Menu_w(QMainWindow):
    def __init__(self):
        super(Menu_w, self).__init__()
        uic.loadUi('menu.ui', self)
        self.addser_bt.clicked.connect(self.addSer_form)
        self.addres_bt.clicked.connect(self.addRes_form)
        self.alltable_bt.clicked.connect(self.getdatabase)
        self.addben_bt.clicked.connect(self.addBen_form)
        self.addser_on_res_bt.clicked.connect(self.addSeronRes_form)
        self.findser_onres_bt.clicked.connect(self.rescalculate_form)
        self.cost_all_bt.clicked.connect(self.show_system_total)
        self.imex_bt.clicked.connect(self.open_import_export_manager)

        self.system_total = update_totalcost_sys()

    def addSer_form(self):
        widget.setCurrentIndex(3)
    def addRes_form(self):
        widget.setCurrentIndex(4)
    def addBen_form(self):
        widget.setCurrentIndex(5)
    def addSeronRes_form(self):
        widget.setCurrentIndex(6)  
    def rescalculate_form(self):
        self.findser = TotalRes_w()
        self.findser.show()    
    def getdatabase(self):
        self.db_viewer = DatabaseViewer()
        self.db_viewer.load_data()
        self.db_viewer.show()
    def open_import_export_manager(self):
        """Mở cửa sổ quản lý Import/Export."""
        self.import_export_manager = ImportExportManager()
        self.import_export_manager.show()
    def show_system_total(self):
        """ Hiển thị tổng số tiền của toàn hệ thống """
        db = mdb.connect('1.db')
        query = db.cursor()
        
        # Tính tổng số tiền của toàn hệ thống
        query.execute("SELECT SUM(total_cost) FROM totalcost_sys")
        system_total = query.fetchone()[0] or 0  # Nếu không có giá trị, trả về 0
        db.close()

        # Hiển thị thông báo
        custom_boxmessagebig(self, "System Total", f"Total revenue of the whole system is {system_total:.2f} $", "icons/money.png")

#Main Login+Register
class MainLogin_w(QMainWindow):
    def __init__(self, widget):
        super(MainLogin_w, self).__init__()
        self.setCentralWidget(widget)
        self.widget = widget

        self.widget.currentChanged.connect(self.update_window_titles_and_icon)

        self.titles = [
            "Residents and Services Management System",
            "Register New User",
            "Menu",
            "New Service",
            "New Resident",
            "Resident's Discount",
            "Add Service on Resident"
        ]
        # Danh sách Icon tương ứng với các giao diện
        self.icons = [
            QIcon(resource_path("icons/home-icon.png")),  
            QIcon(resource_path("icons/register.png")),
            QIcon(resource_path("icons/house menu.png")),
            QIcon(resource_path("icons/newservice.png")),
            QIcon(resource_path("icons/resident.png")),
            QIcon(resource_path("icons/discount-icon.png")),
            QIcon(resource_path("icons/service.png")),  
        ]

        # Cập nhật Icon ban đầu
        self.update_window_titles_and_icon(0)
    def update_window_titles_and_icon(self, index):
        """Cập nhật Icon cửa sổ dựa trên Index của QStackedWidget."""
        if 0 <= index < len(self.icons):
            self.setWindowIcon(self.icons[index])
            self.setWindowTitle(self.titles[index])
   

def update_totalcost_sys():
    db = mdb.connect('1.db')
    query = db.cursor()

    # Lấy danh sách tất cả cư dân và bonus
    query.execute("SELECT last_name, first_name, bonus FROM residents")
    residents = query.fetchall()

    for resident in residents:
        resident_name = resident[0] + " " + resident[1]
        bonus = resident[2]

        query.execute(" SELECT SUM(total_cost) * (1 - '"+str(bonus)+"') FROM orders WHERE name_res =  '"+resident_name+"' ")
        total_cost = query.fetchone()[0] or 0
        query.execute("INSERT INTO totalcost_sys (name, total_cost) VALUES ('"+resident_name+"', '"+str(total_cost)+"') ON CONFLICT (name) DO UPDATE SET total_cost = excluded.total_cost")

    query.execute("SELECT SUM(total_cost) FROM totalcost_sys")
    system_total = query.fetchone()[0] or 0

    db.commit()
    db.close()

    return system_total

#Add Service
class AddSer_w(QMainWindow):
    def __init__(self, widget, add_seron_res_instance):
        super(AddSer_w, self).__init__()
        uic.loadUi('AddService.ui', self)
        self.addnewser_bt.clicked.connect(self.addSer)
        self.enter_shortcut = QShortcut(QtCore.Qt.Key.Key_Return, self)
        self.enter_shortcut.activated.connect(self.addSer)
        self.widget = widget
        self.add_seron_res_instance = add_seron_res_instance
    
    def showEvent(self, event):
        super().showEvent(event)
        # Đặt focus vào trường đầu tiên (user_log)
        self.newsername.setFocus()
    
    def addSer(self):
        sername = self.newsername.text()
        cost = self.newsercost.text()
        db = mdb.connect('1.db')
        query = db.cursor()
        query.execute("select * from services where name='"+sername+"' ")
        kt = query.fetchone()
        
        if kt:
            QMessageBox.warning(self, "Service warning", "Service name already exists")
            widget.setCurrentIndex(3)
        else:
            query.execute("insert into services (name, price) values ('"+sername+"','"+cost+"') ")
            db.commit()
            custom_boxmessagebig(self, "Service Notice", "Service '"+sername+"' added successfully.", "icons/newservice.png")
            db.close()
            self.add_seron_res_instance.load_services()
        widget.setCurrentIndex(2)
        
#Add Resident
class AddRes_w(QMainWindow):
    def __init__(self):
        super(AddRes_w, self).__init__()
        uic.loadUi('AddResident.ui', self)
        self.addnewres_bt.clicked.connect(self.addRes)

        self.enter_shortcut = QShortcut(QtCore.Qt.Key.Key_Return, self)
        self.enter_shortcut.activated.connect(self.addRes)
    def showEvent(self, event):
        super().showEvent(event)
        self.newlname.setFocus()

    def addRes(self):
        lname = self.newlname.text()
        fname = self.newfname.text()
        db = mdb.connect('1.db')
        query = db.cursor()
        query.execute("insert into residents (last_name, first_name) values ('"+lname+"','"+fname+"') ")
        db.commit()
        custom_boxmessagebig(self, "Resident Notice", "Resident "+lname+" "+fname+" added successfully.", "icons/resident.png")
        db.close()
        widget.setCurrentIndex(2)

#Add Benefits
class AddBen_w(QMainWindow):
    def __init__(self):
        super(AddBen_w, self).__init__()
        uic.loadUi('AddBen.ui', self)
        self.addbenpers_bt.clicked.connect(self.addBen)

        self.enter_shortcut = QShortcut(QtCore.Qt.Key.Key_Return, self)
        self.enter_shortcut.activated.connect(self.addBen)
    def showEvent(self, event):
        super().showEvent(event)
        self.IDResben.setFocus()        

    def addBen(self):
        id_ben = self.IDResben.text()
        Perbens = float(self.Perben.text())/100
        if float(self.Perben.text()) > 100 and float(self.Perben.text()) < 0:
            QMessageBox.warning(self, "Discount errors", "The percentage you want to discount is invalid")
            widget.setCurrentIndex(5)
        else:
            db = mdb.connect('1.db')
            query = db.cursor()
            query.execute("select * from residents where ID='"+id_ben+"' ")
            kt = query.fetchone()
            if kt:
                query.execute("update residents SET bonus = '"+str(Perbens)+"' where ID= '"+str(id_ben)+"' ")
                db.commit()
                custom_boxmessagebig(self, "Discount Notice", "Residents with ID "+str(id_ben)+" get discount "+self.Perben.text()+"%.", "icons/discount-icon.png")
                widget.setCurrentIndex(2)
            else:
                QMessageBox.warning(self, "Discount errors", "No match found, please re-enter ID")
                widget.setCurrentIndex(5)

#Show DatabaseViewer
class DatabaseViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Database Viewer")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon('icons/database.png'))

        # Widget chính
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Các thành phần UI
        self.label = QLabel("Select a table:", self.central_widget)
        self.layout.addWidget(self.label)

        self.table_selector = QComboBox(self.central_widget)
        self.table_selector.currentIndexChanged.connect(self.on_table_select)
        self.layout.addWidget(self.table_selector)

        self.load_button = QPushButton("Load Data", self.central_widget)
        self.load_button.clicked.connect(self.load_data)
        self.layout.addWidget(self.load_button)

        self.table_widget = QTableWidget(self.central_widget)
        self.layout.addWidget(self.table_widget)

        self.tables = []

    def connect_to_db(self):
        """ Kết nối đến cơ sở dữ liệu """
        connection = mdb.connect('1.db')
        return connection


    def load_data(self):
        """ Load tables and populate combo box """
        conn = self.connect_to_db()
        if conn is None:
            return

        cursor = conn.cursor()

        try:
            # Truy vấn danh sách bảng trong SQLite
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            # Cập nhật ComboBox với danh sách bảng
            self.tables = [table[0] for table in tables if table[0] != 'user_list']
            self.table_selector.clear()
            self.table_selector.addItems(self.tables)

        
        finally:
            conn.close()


    def on_table_select(self):
        """ Khi người dùng chọn bảng """
        table_name = self.table_selector.currentText()
        if table_name:
            self.load_table_data(table_name)

    def load_table_data(self, table_name):
        """ Hiển thị dữ liệu và cấu trúc bảng """
        conn = self.connect_to_db()
        if conn is None:
            return

        cursor = conn.cursor()

        try:
            # Lấy dữ liệu từ bảng
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()

            if rows:
                # Lấy thông tin cấu trúc bảng
                cursor.execute(f"PRAGMA table_info('{table_name}')")
                columns = cursor.fetchall()
                headers = [col[1] for col in columns]  # col[1] là tên cột

                # Hiển thị dữ liệu trong table widget
                self.table_widget.setRowCount(len(rows))
                self.table_widget.setColumnCount(len(headers))
                self.table_widget.setHorizontalHeaderLabels(headers)

                for row_idx, row in enumerate(rows):
                    for col_idx, value in enumerate(row):
                        self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

        finally:
            conn.close()

#Add Service on Reisdent
class AddSeronRes_w(QMainWindow):
    def __init__(self):
        super(AddSeronRes_w, self).__init__()
        uic.loadUi('AddSeronRes.ui', self)
        self.addseruse_on_res_bt.clicked.connect(self.addSeronRes)
        self.enter_shortcut = QShortcut(QtCore.Qt.Key.Key_Return, self)
        self.enter_shortcut.activated.connect(self.addSeronRes)
        self.back_addseronres_bt.clicked.connect(self.back_to_menu)
        self.load_services()
    
    def showEvent(self, event):
        super().showEvent(event)
        self.IDResuse.setFocus()

    def back_to_menu(self):
        widget.setCurrentIndex(2)

    def load_services(self):
        db = mdb.connect('1.db')
        query = db.cursor()
        query.execute("select name from services")
        namesers = query.fetchall()
        db.close()

        # Xóa tất cả các mục trong ComboBox trước khi tải mới
        self.Seruse.clear()

        for nameser in namesers:
            self.Seruse.addItem(nameser[0])

    def addSeronRes(self):
        id_seraddres = self.IDResuse.text()
        selected_service = self.Seruse.currentText()
        amt = self.amount_seruse.text()
        
        if int(amt) <= 0 or not id_seraddres:
            QMessageBox.warning(self, "Add Service errors", "The information you selected is invalid.")
            widget.setCurrentIndex(6)
        else:
            db = mdb.connect('1.db')
            query = db.cursor()
            
            query.execute("select last_name, first_name, bonus from residents where ID='"+id_seraddres+"' ")
            resident = query.fetchone()
            if not resident:
                QMessageBox.warning(self, "Add services errors", "No match found, please re-enter ID")
                widget.setCurrentIndex(6)
            resident_name = resident[0] + " " + resident[1]
            bonus = resident[2]

            query.execute("select price from services where name='"+selected_service+"' ")
            service = query.fetchone()
            if not service:
                QMessageBox.warning(self, "Errors", "No match found, please re-enter ID")
                widget.setCurrentIndex(6)
            service_price = float(service[0])

            total_price = service_price * float(amt)

            query.execute("INSERT INTO orders (name_res, name_ser, amount, total_cost) values ('"+resident_name+"','"+selected_service+"','"+amt+"','"+str(total_price)+"')")
            db.commit()
            
            query.execute("SELECT SUM(total_cost * (1 - '"+str(bonus)+"')) FROM orders where name_res='"+resident_name+"' ")
            calculres = query.fetchone()
            total_cost = calculres[0] if calculres[0] else 0

            query.execute("INSERT INTO totalcost_sys (name, total_cost) values ('"+resident_name+"','"+str(total_cost)+"') ON CONFLICT (name) DO UPDATE SET total_cost = excluded.total_cost")
            db.commit()
            custom_boxmessagebig(self, "Service Notice", "Add '"+selected_service+"' service for resident named '"+resident_name+"' successfully.", "icons/service.png")

#Calculate the total amount that residents need to pay               
class TotalRes_w(QMainWindow):
    def __init__(self):
        super(TotalRes_w, self).__init__()
        uic.loadUi('TotalRes.ui', self)
        self.setWindowIcon(QIcon('icons/money.png'))
        self.rescalculate_bt.clicked.connect(self.calculate_res)
        self.enter_shortcut = QShortcut(QtCore.Qt.Key.Key_Return, self)
        self.enter_shortcut.activated.connect(self.calculate_res)

    def showEvent(self, event):
        super().showEvent(event)
        self.lnamefind.setFocus()

    def calculate_res(self):
        lname = self.lnamefind.text()
        fname = self.fnamefind.text()
        find_name = lname + " " + fname
        db = mdb.connect('1.db')
        query = db.cursor()
        
        query.execute("select bonus from residents where last_name='"+lname+"' and first_name='"+fname+"' ")
        bonus_find = query.fetchone()
        bonus = bonus_find[0]

        query.execute("SELECT SUM(total_cost * (1 - '"+str(bonus)+"')) FROM orders where name_res='"+find_name+"' ")
        calculres = query.fetchone()
        calculateres = calculres[0]
        custom_boxmessagebig(self, "Total Pay Notice", "Resident "+find_name+" must pay a total of "+str(calculateres)+"$.", "icons/money.png")   
        widget.setCurrentIndex(2)

class ImportExportManager(QMainWindow):
    def __init__(self):
        super(ImportExportManager, self).__init__()
        uic.loadUi('ExIm.ui', self)
        self.setWindowIcon(QIcon('icons/export icon.png'))
        self.ex_bt.clicked.connect(self.export_to_txt)
        self.im_bt.clicked.connect(self.import_from_txt)

        # Kết nối cơ sở dữ liệu và tải danh sách bảng
        self.db = mdb.connect('1.db')
        self.load_table_names()

    def load_table_names(self):
        """Tải danh sách bảng từ cơ sở dữ liệu vào ComboBox."""
        cursor = self.db.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = cursor.fetchall()

        self.tableex_box.clear()
        for table in tables:
            self.tableex_box.addItem(table[0])


    def export_to_txt(self):
        """Xuất dữ liệu từ bảng đã chọn ra file TXT."""
        table_name = self.tableex_box.currentText()
        if not table_name:
            QMessageBox.warning(self, "Export Error", "No table selected!")
            return

        # Hộp thoại để chọn nơi lưu file
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Data", "", "Text Files (*.txt);;All Files (*)")
        if not file_path:
            return  # Hủy nếu không chọn file

        cursor = self.db.cursor()

        # Lấy danh sách cột từ bảng
        cursor.execute(f"PRAGMA table_info({table_name})")  # PRAGMA trả thông tin về cột của bảng
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]  # Tên cột
        num_columns = len(column_names)  # Số lượng cột

        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()

        with open(file_path, "w") as file:
            header_line = f"{table_name} - {num_columns}, " + ", ".join(column_names)
            file.write(header_line + "\n")
            
            for row in data:
                line = " | ".join(map(str, row))
                file.write(line + "\n")

        QMessageBox.information(self, "Export Success", f"Data exported to {file_path}")
      

    def import_from_txt(self):
        # Chọn file TXT
        
        file_path, _ = QFileDialog.getOpenFileName(self, "Import Data", "", "Text Files (*.txt);;All Files (*)")
        if not file_path:
            return  # Hủy nếu không chọn file

        # Hỏi người dùng tên bảng mới
        table_name, ok = QInputDialog.getText(self, "New Table", "Enter name for the new table:")
        if not ok or not table_name.strip():
            QMessageBox.warning(self, "Import Error", "Table name cannot be empty!")
            return

        with open(file_path, "r") as file:
            lines = file.readlines()

        if not lines:
            QMessageBox.warning(self, "Import Error", "The file is empty!")
            return

        # Đọc dòng đầu tiên: số cột và tên cột
        header_line = lines[0].strip()
        header_parts = header_line.split(",")  # Giả sử dòng đầu tiên phân tách bằng dấu phẩy
        if len(header_parts) < 2:
            QMessageBox.warning(self, "Import Error", "Invalid header format!")
            return

        num_columns = int(header_parts[0])  # Số cột
        column_names = header_parts[1:]  # Tên cột
        if len(column_names) != num_columns:
            QMessageBox.warning(self, "Import Error", "Number of columns does not match header definition!")
            return

        # Tạo cấu trúc bảng mới
        column_defs = ", ".join([f"{col} TEXT" for col in column_names])  # Mặc định mọi cột là TEXT
        cursor = self.db.cursor()
        cursor.execute(f"CREATE TABLE {table_name} ({column_defs})")
        self.db.commit()

        # Chèn dữ liệu từ các dòng còn lại
        for line in lines[1:]:
            values = line.strip().split(" | ")  # Tách dữ liệu bằng " | "
            if len(values) != num_columns:
                QMessageBox.warning(self, "Import Error", f"Invalid data row: {line}")
                continue
            placeholders = ", ".join(["?" for _ in values])
            cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", values)

        self.db.commit()
        QMessageBox.information(self, "Import Success", f"Table '{table_name}' created and data imported successfully!")

        # Cập nhật danh sách bảng trong ComboBox
        self.load_table_names()


    def closeEvent(self, event):
        """Đóng kết nối cơ sở dữ liệu khi ứng dụng tắt."""
        self.db.close()
        super().closeEvent(event)

#Process

def create_app():
    
    # Tạo các giao diện
    Login_f = Login_w()
    Reg_f = Reg_w()
    Menu_f = Menu_w()
    AddSeronRes_f = AddSeronRes_w()
    AddSer_f = AddSer_w(widget, AddSeronRes_f)
    AddRes_f = AddRes_w()
    AddBen_f = AddBen_w()
    

    # Thêm giao diện vào QStackedWidget
    widget.addWidget(Login_f)
    widget.addWidget(Reg_f)
    widget.addWidget(Menu_f)
    widget.addWidget(AddSer_f)
    widget.addWidget(AddRes_f)
    widget.addWidget(AddBen_f)
    widget.addWidget(AddSeronRes_f)

    # Đặt giao diện đầu tiên
    widget.setCurrentIndex(0)
    widget.setFixedHeight(500)
    widget.setFixedWidth(700)
    return widget

# Run
if __name__ == "__main__":
    app = QApplication([])
    global widget
    widget = QStackedWidget()
    # Khởi tạo QStackedWidget và lớp quản lý chính
    stacked_widget = create_app()
    main_app = MainLogin_w(stacked_widget)
    main_app.show()

    app.exec()












