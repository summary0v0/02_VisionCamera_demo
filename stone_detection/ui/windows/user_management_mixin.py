from .dependencies import *


class UserManagementMixin:
    def load_user_table(self):
        # 查询用户信息
        users = get_all_users()     # # 函数没写？

        # 清空表格
        self.userInfoTable.setRowCount(len(users))

        for row_idx, user in enumerate(users):
            # 列顺序: 用户名、用户密码、用户权限、最后登录时间、创建时间、修改时间
            # 用户密码这里留空或显示为 '******'
            username_item = QTableWidgetItem(str(user.get("username", "")))
            fullname_item = QTableWidgetItem(str(user.get("fullname", "")))
            password_item = QTableWidgetItem("******")  # 因为没有查询密码
            role_item = QTableWidgetItem(str(user.get("role", "")))
            last_login_item = QTableWidgetItem(
                str(user.get("lastLogin_at", "")) if user.get("lastLogin_at") else ""
            )
            created_item = QTableWidgetItem(
                str(user.get("created_at", "")) if user.get("created_at") else ""
            )
            updated_item = QTableWidgetItem(
                str(user.get("updated_at", "")) if user.get("updated_at") else ""
            )

            # 设置每个单元格的字体（可选）
            font12 = self.userInfoTable.font()  # 或你之前定义的 font12
            for item in [
                username_item,
                fullname_item,
                password_item,
                role_item,
                last_login_item,
                created_item,
                updated_item,
            ]:
                item.setFont(font12)

            # 将每个 QTableWidgetItem 写入表格
            self.userInfoTable.setItem(row_idx, 0, username_item)
            self.userInfoTable.setItem(row_idx, 1, fullname_item)
            self.userInfoTable.setItem(row_idx, 2, password_item)
            self.userInfoTable.setItem(row_idx, 3, role_item)
            self.userInfoTable.setItem(row_idx, 4, last_login_item)
            self.userInfoTable.setItem(row_idx, 5, created_item)
            self.userInfoTable.setItem(row_idx, 6, updated_item)
        self.center_table_data(self.userInfoTable)

    def on_delete_user_clicked(self):
        selected_rows = self.userInfoTable.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "提示", "请先选中要删除的用户")
            return

        reply = QMessageBox.question(
            self, "确认删除",
            "确定要删除选中的用户吗？",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        # 倒序遍历删除，从最后一行往前删，不会影响前面行的索引，这是处理列表/表格删除的标准做法。
        for index in sorted(selected_rows, key=lambda x: x.row  (), reverse=True):
            row = index.row()
            username_item = self.userInfoTable.item(row, 0)
            if username_item:
                username = username_item.text()
                success, msg = delete_user(username, self.current_user_role)
                QMessageBox.information(self, "删除结果", msg)

                # 写日志
                log_user_action(
                    username=self.current_user,  # 当前操作人
                    action_type="delete_user",
                    target_user=username,
                    result=msg
                )
                if success:
                    self.userInfoTable.removeRow(row)

    def on_update_user_clicked(self):
        selected_rows = self.userInfoTable.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "提示", "请先选中要修改的用户")
            return

        index = selected_rows[0]
        row = index.row()
        username_item = self.userInfoTable.item(row, 0)
        fullname_item = self.userInfoTable.item(row, 1)
        password_item = self.userInfoTable.item(row, 2)
        role_item = self.userInfoTable.item(row, 3)

        target_username = username_item.text()
        new_fullname = fullname_item.text()
        new_role = role_item.text() if role_item else None
        password_text = password_item.text() if password_item else ""
        new_password_hash = None

        # 仅在密码被修改（不是 "******"）时才 hash
        if password_text != "******" and password_text.strip() != "":
            new_password_hash = hash_password(password_text)

        success, msg, log_msg = update_user(
            target_username=target_username,
            current_user_role=self.current_user_role,
            new_password_hash=new_password_hash,
            new_role=new_role,
            new_fullname=new_fullname

        )
        QMessageBox.information(self, "修改结果", msg)

        # 写日志
        log_user_action(
            username=self.current_user,  # 当前操作人
            action_type="update_user",
            target_user=target_username,
            result=log_msg
        )

        if success:
            if new_role:
                self.userInfoTable.item(row, 3).setText(new_role)
            if new_password_hash:
                self.userInfoTable.item(row, 2).setText("******")
            if new_fullname:
                self.userInfoTable.item(row, 1).setText(new_fullname)
