from PyQt5.QtWidgets import QWidget

from ..generated.tip import Ui_Tip


class TipWin(QWidget, Ui_Tip):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.close)
        self.pushButton_2.clicked.connect(self.close)


__all__ = ["TipWin"]

