import sys
from PyQt6.QtWidgets import QApplication
from config_manager import ConfigManager
from theme_manager import ThemeManager
from PyQt6.QtGui import QIcon
from ui import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    app_icon = QIcon('atc.png')
    app.setWindowIcon(app_icon)
    
    config_manager = ConfigManager('config.yaml')
    theme_manager = ThemeManager(config_manager.get_themes_dir())
    
    window = MainWindow(config_manager, theme_manager)
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()