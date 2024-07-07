from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QListWidget, QPushButton, QLabel, QLineEdit, QMessageBox, QApplication)
from PyQt6.QtGui import QFont, QKeyEvent
from PyQt6.QtCore import Qt
from utils import restart_alacritty

class MainWindow(QMainWindow):
    def __init__(self, config_manager, theme_manager):
        super().__init__()
        self.config_manager = config_manager
        self.theme_manager = theme_manager
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Alacritty Theme Changer")
        self.setGeometry(100, 100, 800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        title_label = QLabel("Alacritty Theme Changer")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(title_label)
        
        self.current_theme_input = QLineEdit()
        self.current_theme_input.setReadOnly(True)
        layout.addWidget(self.current_theme_input)
        
        self.theme_list = QListWidget()
        font = self.theme_list.font()
        font.setPointSize(int(font.pointSize() * 1.5))
        self.theme_list.setFont(font)
        themes = sorted(self.theme_manager.get_themes())
        self.theme_list.addItems(themes)
        self.theme_list.itemDoubleClicked.connect(self.apply_theme)
        self.theme_list.keyPressEvent = self.theme_list_key_press
        layout.addWidget(self.theme_list)
        
        button_layout = QHBoxLayout()
        
        apply_button = QPushButton("Apply Theme")
        apply_button.clicked.connect(self.apply_theme)
        button_layout.addWidget(apply_button)
        
        restart_button = QPushButton("Restart Alacritty")
        restart_button.clicked.connect(self.restart_alacritty)
        button_layout.addWidget(restart_button)
        
        about_button = QPushButton("About")
        about_button.clicked.connect(self.show_about)
        button_layout.addWidget(about_button)
        
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        
        central_widget.setLayout(layout)
        
        self.update_current_theme()
    
    def show_about(self):
        about_text = """
        Alacritty Theme Changer
        
        A simple GUI application to change Alacritty themes.
        GitHub: https://github.com/lhassan-aitmouss/alacritty-theme-switcher
        Created by Lhassan Ait Mouss
        """
        QMessageBox.about(self, "About", about_text)
    
    def apply_theme(self):
        selected_theme = self.theme_list.currentItem().text()
        self.theme_manager.update_alacritty_config(
            self.config_manager.get_alacritty_conf_file(), 
            selected_theme
        )
        self.update_current_theme()
    
    def restart_alacritty(self):
        restart_alacritty()
    
    def update_current_theme(self):
        current_theme = self.theme_manager.get_current_theme(
            self.config_manager.get_alacritty_conf_file()
        )
        self.current_theme_input.setText(current_theme or "No theme selected")
        
        if current_theme:
            items = self.theme_list.findItems(current_theme, Qt.MatchFlag.MatchExactly)
            if items:
                self.theme_list.setCurrentItem(items[0])

    def theme_list_key_press(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Space:
            self.apply_theme()
        else:
            super(QListWidget, self.theme_list).keyPressEvent(event)