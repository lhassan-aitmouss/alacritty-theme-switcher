import os
import re

class ThemeManager:
    def __init__(self, themes_dir):
        self.themes_dir = themes_dir
    
    def get_themes(self):
        return [f for f in os.listdir(self.themes_dir) if f.endswith('.toml')]
    
    def update_alacritty_config(self, alacritty_conf_file, selected_theme):
        theme_path = os.path.join(self.themes_dir, selected_theme)
        with open(alacritty_conf_file, 'r') as file:
            config = file.read()
        
        import_line = re.search(r'import\s*=\s*\[(.*?)\]', config, re.DOTALL)
        if import_line:
            new_import = f'import = ["{theme_path}"]'
            config = config.replace(import_line.group(0), new_import)
        else:
            config += f'\nimport = ["{theme_path}"]'
        
        with open(alacritty_conf_file, 'w') as file:
            file.write(config)

    def get_current_theme(self, alacritty_conf_file):
        with open(alacritty_conf_file, 'r') as file:
            config = file.read()
        
        import_line = re.search(r'import\s*=\s*\[(.*?)\]', config, re.DOTALL)
        if import_line:
            theme_path = import_line.group(1).strip('"')
            return os.path.basename(theme_path)
        return None