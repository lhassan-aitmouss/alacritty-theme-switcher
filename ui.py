from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QListWidget, QPushButton, QLabel, QLineEdit, QDialog, QFileDialog, QApplication)
from PyQt6.QtGui import QFont, QKeyEvent, QIcon, QScreen
from PyQt6.QtCore import Qt
from utils import restart_alacritty

class ConfigDialog(QDialog):
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Settingss")
        self.setFixedSize(640, 200)
        self.setWindowIcon(QIcon('atc.png'))

        layout = QVBoxLayout()

        # Alacritty config file
        config_layout = QHBoxLayout()
        config_layout.addWidget(QLabel("Alacritty config file:"))
        self.config_input = QLineEdit(self.config_manager.get_alacritty_conf_file())
        config_layout.addWidget(self.config_input)
        config_button = QPushButton("Browse")
        config_button.clicked.connect(self.browse_config)
        config_layout.addWidget(config_button)
        layout.addLayout(config_layout)

        # Themes directory
        themes_layout = QHBoxLayout()
        themes_layout.addWidget(QLabel("Themes directory:"))
        self.themes_input = QLineEdit(self.config_manager.get_themes_dir())
        themes_layout.addWidget(self.themes_input)
        themes_button = QPushButton("Browse")
        themes_button.clicked.connect(self.browse_themes)
        themes_layout.addWidget(themes_button)
        layout.addLayout(themes_layout)

        # Save and Cancel buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_config)
        button_layout.addWidget(save_button)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def browse_config(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Alacritty config file", "", "TOML Files (*.toml)")
        if file_name:
            self.config_input.setText(file_name)

    def browse_themes(self):
        dir_name = QFileDialog.getExistingDirectory(self, "Select Themes Directory")
        if dir_name:
            self.themes_input.setText(dir_name)

    def save_config(self):
        self.config_manager.update_config(
            self.config_input.text(),
            self.themes_input.text()
        )
        self.accept()


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Alacritty Theme Changer")
        self.setFixedSize(480, 200)

        layout = QVBoxLayout()
        
        about_text = """
        <h2>Alacritty Theme Changer</h2>
        <p>A simple GUI application to change Alacritty themes.</p>
        <p>GitHub: <a href="https://github.com/lhassan-aitmouss/alacritty-theme-switcher">
        https://github.com/lhassan-aitmouss/alacritty-theme-switcher</a></p>
        <p>Created by Lhassan Ait Mouss</p>
        """
        
        label = QLabel(about_text)
        label.setOpenExternalLinks(True)
        label.setTextFormat(Qt.TextFormat.RichText)
        label.setWordWrap(True)
        
        layout.addWidget(label)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self, config_manager, theme_manager):
        super().__init__()
        self.config_manager = config_manager
        self.theme_manager = theme_manager
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Alacritty Theme Changer")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon('icon.png'))
        self.center()

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
        
        settings_button = QPushButton("Settings")
        settings_button.clicked.connect(self.show_settings)
        button_layout.addWidget(settings_button)

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
    
    def show_settings(self):
        dialog = ConfigDialog(self.config_manager)
        if dialog.exec():
            # Reload themes if settings were changed
            self.theme_list.clear()
            themes = sorted(self.theme_manager.get_themes())
            self.theme_list.addItems(themes)
            self.update_current_theme()

    def center(self):
        qr = self.frameGeometry()
        cp = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def show_about(self):
        dialog = AboutDialog(self)
        dialog.exec()

    
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