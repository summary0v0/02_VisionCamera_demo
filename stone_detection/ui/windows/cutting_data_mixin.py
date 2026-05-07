from .dependencies import *


class CuttingDataMixin:
    def on_cut_start_date_changed(self):
        self.cutEndDateEdit.setMinimumDate(self.cutStartDateEdit.date())

    def reset_date_range(self):
        """将日期重置：起始2025-09-01，结束今天"""
        self.cutStartDateEdit.setDate(QDate(2025, 9, 1))
        today = datetime.today()
        self.cutEndDateEdit.setDate(QDate(today.year, today.month, today.day))

    def query_cutting_data(self):
        """根据时间范围查询切割数据并填充表格"""
        start_date = self.cutStartDateEdit.date().toString("yyyy-MM-dd") + " 00:00:00"
        end_date = self.cutEndDateEdit.date().toString("yyyy-MM-dd") + " 23:59:59"

        # 调用查询函数
        records = get_cutting_records(start_date, end_date)

        # 设置表格行数
        self.cutDataTable.setRowCount(len(records))

        # 设置表格内容
        for row_idx, rec in enumerate(records):
            items = [
                rec.get("operator_fullname", ""),
                rec.get("project_name", ""),
                rec.get("length", 0),
                rec.get("width", 0),
                rec.get("thickness", 0),
                rec.get("cutting_meters", 0),
                rec.get("square_area", 0),
                rec.get("cutting_status", ""),
                str(rec.get("cutting_time", "")) if rec.get("cutting_time") else "",
                rec.get("drawing_number", ""),
                rec.get("box_number", "")
            ]
            for col_idx, value in enumerate(items):
                item = QTableWidgetItem(str(value))
                self.cutDataTable.setItem(row_idx, col_idx, item)
        # 居中表格数据
        self.center_table_data(self.cutDataTable)
