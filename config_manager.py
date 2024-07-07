import yaml

class ConfigManager:
    def __init__(self, config_path):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        
    def get_alacritty_conf_file(self):
        return self.config['alacritty_conf_file']
    
    def get_themes_dir(self):
        return self.config['themes_dir']