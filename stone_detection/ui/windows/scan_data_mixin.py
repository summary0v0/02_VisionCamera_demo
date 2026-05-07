from .dependencies import *


class ScanDataMixin:
    def on_scan_view_large(self):
        cid = getattr(self, "current_scan_composite_identifier", None)   # 获取当前选中的数据行标识符 (cid)
        if not cid:
            QMessageBox.warning(self, "提示", "未选中行！")
            return

        urls = query_image_urls(cid)
        if not urls:
            QMessageBox.warning(self, "提示", "图片不存在！")
            return

        # 根据按钮选择要打开的图片
        file_path = None
        if self.scanOriginalBtn.isChecked() and urls.get("original_url"):
            local_path = urls["original_url"]
            if os.path.exists(local_path):
                file_path = local_path
            else:
                QMessageBox.warning(self, "提示", "图片不存在！")
        elif self.scanRulerBtn.isChecked() and urls.get("scale_url"):
            url = urls["scale_url"]
            # 量尺图片是网络图片，需要先下载到临时文件

            try:
                import requests
                from tempfile import NamedTemporaryFile
                response = requests.get(url)        # 发送 HTTP GET 请求下载图片内容。
                temp_file = NamedTemporaryFile(delete=False, dir=download_dir, suffix=".png")
                temp_file.write(response.content)
                temp_file.close()
                file_path = temp_file.name
            except Exception as e:
                print(f"下载量尺图片失败: {e}")
                return

        if file_path:
            # 调用系统默认图片查看器打开
            if platform.system() == "Darwin":  # macOS
                subprocess.call(["open", file_path])
            elif platform.system() == "Windows":  # Windows
                os.startfile(file_path)
            else:  # Linux
                subprocess.call(["xdg-open", file_path])

    def refresh_scan_image(self, type: str):
        # 设置按钮状态
        if type == "original":
            self.scanOriginalBtn.setChecked(True)
            self.scanRulerBtn.setChecked(False)
        elif type == "ruler":
            self.scanOriginalBtn.setChecked(False)
            self.scanRulerBtn.setChecked(True)

        # 直接读取 self.current_scan_composite_identifier
        cid = getattr(self, "current_scan_composite_identifier", None)
        if not cid:
            self.scanPicView.setScene(QGraphicsScene())
            return

        urls = query_image_urls(cid)  # 调用外部函数查询数据库，获取该 cid 对应的图片 URL/本地路径字典。
        if not urls:
            print(f"{cid} 未找到对应图片")
            self.scanPicView.setScene(QGraphicsScene())
            return

        pixmap = None
        if self.scanOriginalBtn.isChecked() and urls.get("original_url"):
            local_path = urls["original_url"]
            if os.path.exists(local_path):
                pixmap = QPixmap(local_path)
            else:
                print(f"原始图片路径不存在: {local_path}")
        elif self.scanRulerBtn.isChecked() and urls.get("scale_url"):
            url = urls["scale_url"]
            try:
                response = requests.get(url)
                img_data = BytesIO(response.content)
                pixmap = QPixmap()
                pixmap.loadFromData(img_data.read())
            except Exception as e:
                print(f"加载量尺图片失败: {e}")

        # 显示到 QGraphicsView
        scene = QGraphicsScene()
        if pixmap:
            pixmap = pixmap.scaled(
                self.scanPicView.width(), self.scanPicView.height(),
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            scene.addPixmap(pixmap)
        self.scanPicView.setScene(scene)

    def on_scan_table_row_selected(self, row, column):
        # 获取 composite_identifier（和之前一样）
        production_order_number = self.scanDataTable.item(row, 1).text()
        number = self.scanDataTable.item(row, 2).text()
        composite_identifier = f"{production_order_number}{number}"
        self.current_scan_composite_identifier = composite_identifier  # ✅ 必须加上
        self.refresh_scan_image("original" if self.scanOriginalBtn.isChecked() else "ruler")

        urls = query_image_urls(composite_identifier)
        if not urls:
            print(f"{composite_identifier} 未找到对应图片")
            # 清空 QGraphicsView
            scene = QGraphicsScene()
            self.scanPicView.setScene(scene)
            return

        pixmap = None

        if self.scanOriginalBtn.isChecked() and urls.get("original_url"):
            local_path = urls["original_url"]
            if os.path.exists(local_path):
                pixmap = QPixmap(local_path)
            else:
                print(f"原始图片路径不存在: {local_path}")
        elif self.scanRulerBtn.isChecked() and urls.get("scale_url"):
            url = urls["scale_url"]
            try:
                response = requests.get(url)
                img_data = BytesIO(response.content)
                pixmap = QPixmap()
                pixmap.loadFromData(img_data.read())   # 从内存数据中加载图片，而不是从文件路径加载。
            except Exception as e:
                print(f"加载量尺图片失败: {e}")

        # 显示到 QGraphicsView
        scene = QGraphicsScene()
        if pixmap:
            # 按比例缩放适应 QGraphicsView 尺寸
            view_width = self.scanPicView.width()
            view_height = self.scanPicView.height()
            pixmap = pixmap.scaled(view_width, view_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            scene.addPixmap(pixmap)
        self.scanPicView.setScene(scene)

    def load_table_data(self):
        """
        查询数据库并填充到 scanDataTable
        """
        # 获取时间范围
        start_time = self.scanStartDateEdit.date().toString("yyyy-MM-dd")  + " 00:00:00"
        end_time = self.scanEndDateEdit.date().toString("yyyy-MM-dd")  + " 23:59:59"

        # 查询数据库
        results = query_stone_measurements(start_time, end_time)

        # 设置表格行数
        self.scanDataTable.setRowCount(len(results))

        for row_idx, row in enumerate(results):
            # -------- 1. 图片列 --------
            img_label = QLabel()
            img_label.setAlignment(Qt.AlignCenter)
            # 检查数据库返回的数据中是否有原始图片 URL 并且该本地文件确实存在。
            if row["original_url"] and os.path.exists(row["original_url"]):
                pixmap = QPixmap(row["original_url"]).scaled(
                    250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
                img_label.setPixmap(pixmap)
            else:
                img_label.setText("无图片")
            self.scanDataTable.setCellWidget(row_idx, 0, img_label)

            # -------- 2. 单号 --------
            self.scanDataTable.setItem(row_idx, 1, QTableWidgetItem(str(row["production_order_number"])))

            # -------- 3. ID（编号前缀 + 编号）--------
            id_value = (row["number_prefix"] or "") + str(row["number"])
            self.scanDataTable.setItem(row_idx, 2, QTableWidgetItem(id_value))

            # -------- 4. 长 --------
            self.scanDataTable.setItem(row_idx, 3, QTableWidgetItem(str(row["design_length"])))

            # -------- 5. 宽 --------
            self.scanDataTable.setItem(row_idx, 4, QTableWidgetItem(str(row["design_width"])))

            # -------- 6. 扫描长 --------
            self.scanDataTable.setItem(row_idx, 5, QTableWidgetItem(str(row["scan_length"])))

            # -------- 7. 扫描宽 --------
            self.scanDataTable.setItem(row_idx, 6, QTableWidgetItem(str(row["scan_width"])))

            # -------- 8. 扫描时间 --------
            self.scanDataTable.setItem(row_idx, 7, QTableWidgetItem(str(row["scan_time"])))

        # 自适应列宽
        self.scanDataTable.resizeColumnsToContents()
        self.scanDataTable.resizeRowsToContents()
        for col_idx in range(1, self.scanDataTable.columnCount()):
            self.scanDataTable.setColumnWidth(col_idx, 100)  # 从第二列开始固定宽度

        # 居中内容
        self.center_table_data(self.scanDataTable)

    def on_scan_start_date_changed(self):
        self.scanEndDateEdit.setMinimumDate(self.scanStartDateEdit.date())
