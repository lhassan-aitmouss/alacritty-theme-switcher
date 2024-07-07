import sys
import os
import yaml
import subprocess
import re
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QListWidget, QPushButton, QLabel)
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt

class ConfigManager:
    def __init__(self, config_path):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        
    def get_alacritty_conf_file(self):
        return self.config['alacritty_conf_file']
    
    def get_themes_dir(self):
        return self.config['themes_dir']

class ThemeManager:
    def __init__(self, themes_dir):
        self.themes_dir = themes_dir
    
    def get_themes(self):
        return [f for f in os.listdir(self.themes_dir) if f.endswith('.toml')]
    
    def update_alacritty_config(self, alacritty_conf_file, selected_theme):
        theme_path = os.path.join(self.themes_dir, selected_theme)
        with open(alacritty_conf_file, 'r') as file:
            config = file.read()

        # Recherche la ligne d'import existante
        import_line = re.search(r'import\s*=\s*\[(.*?)\]', config, re.DOTALL)
        if import_line:
            # Remplace l'ancien thème par le nouveau
            new_import = f'import = ["{theme_path}"]'
            config = config.replace(import_line.group(0), new_import)
        else:
            # Si aucune ligne d'import n'existe, ajoutez-en une nouvelle
            config += f'\nimport = ["{theme_path}"]'

        with open(alacritty_conf_file, 'w') as file:
            file.write(config)


class AlacrittyRestarter:
    @staticmethod
    def restart():
        subprocess.run(["pkill", "alacritty"])
        subprocess.Popen(["alacritty"])

class MainWindow(QMainWindow):
    def __init__(self, config_manager, theme_manager):
        super().__init__()
        self.config_manager = config_manager
        self.theme_manager = theme_manager
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Alacritty Theme Changer")
        self.setGeometry(100, 100, 400, 500)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        title_label = QLabel("Alacritty Theme Changer")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(title_label)
        
        self.theme_list = QListWidget()
        self.theme_list.addItems(self.theme_manager.get_themes())
        layout.addWidget(self.theme_list)
        
        button_layout = QHBoxLayout()
        
        apply_button = QPushButton("Apply Theme")
        apply_button.clicked.connect(self.apply_theme)
        button_layout.addWidget(apply_button)
        
        restart_button = QPushButton("Restart Alacritty")
        restart_button.clicked.connect(self.restart_alacritty)
        button_layout.addWidget(restart_button)
        
        layout.addLayout(button_layout)
        
        central_widget.setLayout(layout)
    
    def apply_theme(self):
        selected_theme = self.theme_list.currentItem().text()
        self.theme_manager.update_alacritty_config(
            self.config_manager.get_alacritty_conf_file(), 
            selected_theme
        )
    
    def restart_alacritty(self):
        AlacrittyRestarter.restart()

def main():
    app = QApplication(sys.argv)
    
    config_manager = ConfigManager('config.yaml')
    theme_manager = ThemeManager(config_manager.get_themes_dir())
    
    window = MainWindow(config_manager, theme_manager)
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()