try:
    from .ui.generated.interface import Ui_MainWindow
except ImportError:
    from ui.generated.interface import Ui_MainWindow


__all__ = ["Ui_MainWindow"]

