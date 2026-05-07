from HTMLTable import HTMLTable

class HtmlTableApi(object):

    def __init__(self,title:str,header_data:tuple,rows_data:tuple):
        """
        :param title: 表单的标题
        :param header_data: 表头
        :param rows_data: 表的数据
        """
        self.title = title
        self.table = HTMLTable(caption=title,rows=())
        self.table.append_header_rows(rows=header_data)
        self.table.append_data_rows(rows=rows_data)

    def setStyle(self,align ="center",cursor = "pointer",color='#999990'):
        """
        可以自己添加想要的样式
        :param align: 居中、右、左
        :param cursor: 鼠标光标样式
        :param color: 标题颜色
        :return:
        """
        caption_style = {
            'text-align': align,
            'cursor': cursor,
            "color" : color
        }
        self.table.set_style(style=caption_style)
    def setBorderStyle(self):
        """
        设置单元格边框、单元格样式
        :return:
        """
        border_style = {
            'border-color': '#000',
            'border-width': '1px',
            'border-style': 'solid',
            'border-collapse': 'collapse',
            # 实现表格居中
            'margin': 'auto',
        }
        # 外边框
        self.table.set_style(border_style)
        # 单元格边框
        self.table.set_cell_style(border_style)
    def setCellStyle(self):
        """
        设置单元格内容样式
        :return:
        """
        cell_style = {
            'text-align': 'center',
            'padding': '4px',
            'background-color': '#ffffff',
            'font-size': '0.95em',
        }
        self.table.set_cell_style(cell_style)
    def setTableHeaderStyle(self):
        """
        设置表头内容样式
        :return:
        """
        header_cell_style = {
            'text-align': 'center',
            'padding': '4px',
            'background-color': '#aae1fe',
            'color': '#FFFFFF',
            'font-size': '0.95em',
        }
        self.table.set_header_cell_style(header_cell_style)

    def setValueStyle(self):
        """
        判断值，并设置颜色
        :return:
        """
        for row in self.table.iter_data_rows():
            age = row[3].value  #每行第四列的值
            if float(age) < 20:
                row[3].set_style({
                    'background-color': '#ffd001',  #设置样式
                })

    def setAllStyle(self):
        self.setCellStyle()
        self.setTableHeaderStyle()
        self.setStyle(cursor="hand")
        self.setBorderStyle()
        # self.setValueStyle()

    def createHtml(self):
        """
        如果含link,则处理成为可以点击的链接
        :return:
        """
        html = self.table.to_html().replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"')
        with open(r"D:\石材检测\结果/" + self.title+".html","w",encoding="gbk") as f:
            f.write(html)
