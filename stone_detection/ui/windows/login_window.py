import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
import datetime
from ...services import database as dbFunction
LOG_DIR = "log"
LOG_FILE = "log_user_action.log"

def log_user_action(action: str, username: str, detail: str = ""):
    """记录用户操作日志"""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    log_path = os.path.join(LOG_DIR, LOG_FILE)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] 用户: {username} | 操作: {action} | 结果: {detail} \n"

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(log_line)

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("登录 / 注册 / 修改密码")
        self.setGeometry(600, 300, 400, 300)

        # 设置全局字体大小
        self.font = QFont("微软雅黑", 12)
        self.setFont(self.font)

        self.stacked_widget = QStackedWidget()
        self.init_login_page()
        self.init_register_page()
        self.init_change_pwd_page()

        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

    # ---------------- 登录页面 ----------------
    def init_login_page(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(10)

        self.login_user = QLineEdit()
        self.login_pwd = QLineEdit()
        self.login_pwd.setEchoMode(QLineEdit.Password)
        for line in [self.login_user, self.login_pwd]:
            line.setFont(self.font)
            line.setFixedHeight(30)

        layout.addWidget(QLabel("用户名:"))
        layout.addWidget(self.login_user)
        layout.addWidget(QLabel("密码:"))
        layout.addWidget(self.login_pwd)

        # 按钮布局
        btn_layout = QHBoxLayout()
        btn_login = QPushButton("登录")
        btn_register_page = QPushButton("注册")
        btn_change_pwd_page = QPushButton("修改密码")
        for btn in [btn_login, btn_register_page, btn_change_pwd_page]:
            btn.setFont(self.font)
            btn.setFixedHeight(35)
        btn_layout.addWidget(btn_login)
        btn_layout.addWidget(btn_register_page)
        btn_layout.addWidget(btn_change_pwd_page)
        layout.addLayout(btn_layout)

        widget.setLayout(layout)
        self.stacked_widget.addWidget(widget)

        # 信号连接
        btn_login.clicked.connect(self.handle_login)
        btn_register_page.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        btn_change_pwd_page.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))

    # ---------------- 注册页面 ----------------
    def init_register_page(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(10)

        self.reg_user = QLineEdit()
        self.reg_pwd = QLineEdit()
        self.reg_pwd.setEchoMode(QLineEdit.Password)
        self.reg_fullname = QLineEdit()
        for line in [self.reg_user, self.reg_pwd, self.reg_fullname]:
            line.setFont(self.font)
            line.setFixedHeight(30)

        layout.addWidget(QLabel("登录用户名:"))
        layout.addWidget(self.reg_user)
        layout.addWidget(QLabel("密码:"))
        layout.addWidget(self.reg_pwd)
        layout.addWidget(QLabel("中文姓名:"))
        layout.addWidget(self.reg_fullname)

        btn_layout = QHBoxLayout()
        btn_confirm = QPushButton("确认注册")
        btn_back = QPushButton("返回登录")
        for btn in [btn_confirm, btn_back]:
            btn.setFont(self.font)
            btn.setFixedHeight(35)
        btn_layout.addWidget(btn_confirm)
        btn_layout.addWidget(btn_back)
        layout.addLayout(btn_layout)

        widget.setLayout(layout)
        self.stacked_widget.addWidget(widget)

        btn_confirm.clicked.connect(self.handle_register)
        btn_back.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

    # ---------------- 修改密码页面 ----------------
    def init_change_pwd_page(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(10)

        self.change_user = QLineEdit()
        self.change_oldpwd = QLineEdit()
        self.change_oldpwd.setEchoMode(QLineEdit.Password)
        self.change_newpwd = QLineEdit()
        self.change_newpwd.setEchoMode(QLineEdit.Password)
        for line in [self.change_user, self.change_oldpwd, self.change_newpwd]:
            line.setFont(self.font)
            line.setFixedHeight(30)

        layout.addWidget(QLabel("用户名:"))
        layout.addWidget(self.change_user)
        layout.addWidget(QLabel("旧密码:"))
        layout.addWidget(self.change_oldpwd)
        layout.addWidget(QLabel("新密码:"))
        layout.addWidget(self.change_newpwd)

        btn_layout = QHBoxLayout()
        btn_confirm = QPushButton("确认修改密码")
        btn_back = QPushButton("返回登录")
        for btn in [btn_confirm, btn_back]:
            btn.setFont(self.font)
            btn.setFixedHeight(35)
        btn_layout.addWidget(btn_confirm)
        btn_layout.addWidget(btn_back)
        layout.addLayout(btn_layout)

        widget.setLayout(layout)
        self.stacked_widget.addWidget(widget)

        btn_confirm.clicked.connect(self.handle_change_pwd)
        btn_back.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

    # ---------------- 功能方法 ----------------
    def handle_login(self):
        username = self.login_user.text()
        password = self.login_pwd.text()
        flag = dbFunction.check_login(username, password)
        if flag == 1:
            role = dbFunction.get_user_role(username)
            log_user_action("登录", username, "成功")
            self.open_main_window(username, role)
        elif flag == 0:
            log_user_action("登录", username, "失败：权限不足")
            QMessageBox.warning(self, "错误", "登录失败，权限不足！")
        elif flag == -1:
            log_user_action("登录", username, "失败：用户名或密码错误")
            QMessageBox.warning(self, "错误", "登录失败，用户名或密码错误！")

    def handle_register(self):
        username = self.reg_user.text()
        password = self.reg_pwd.text()
        fullname = self.reg_fullname.text()
        if not username or not password or not fullname:
            QMessageBox.warning(self, "错误", "请填写完整信息！")
            return
        if dbFunction.register_user(username, fullname, password):
            log_user_action("注册", username, f"成功，姓名: {fullname}")
            QMessageBox.information(self, "成功", "注册成功！")
            self.stacked_widget.setCurrentIndex(0)
        else:
            log_user_action("注册", username, f"失败，姓名: {fullname} 已存在")
            QMessageBox.warning(self, "错误", "注册失败，用户名或姓名已存在！")

    def handle_change_pwd(self):
        username = self.change_user.text()
        old_password = self.change_oldpwd.text()
        new_password = self.change_newpwd.text()
        if not username or not old_password or not new_password:
            QMessageBox.warning(self, "错误", "请填写完整信息！")
            return
        if dbFunction.change_password(username, old_password, new_password):
            log_user_action("修改密码", username, "成功")
            QMessageBox.information(self, "成功", "密码修改成功！")
            self.stacked_widget.setCurrentIndex(0)
        else:
            log_user_action("修改密码", username, "失败：用户名或原密码错误")
            QMessageBox.warning(self, "错误", "修改失败，用户名或原密码错误！")

    def open_main_window(self, username, role):
        from .main_window import Window
        self.main_window = Window(current_user=username, current_user_role=role)
        self.main_window.showMaximized()
        self.close()
