import yaml

class ConfigManager:
    def __init__(self, config_path):
        self.config_path = config_path
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        
    def get_alacritty_conf_file(self):
        return self.config['alacritty_conf_file']
    
    def get_themes_dir(self):
        return self.config['themes_dir']
    
    def update_config(self, alacritty_conf_file, themes_dir):
        self.config['alacritty_conf_file'] = alacritty_conf_file
        self.config['themes_dir'] = themes_dir
        with open(self.config_path, 'w') as file:
            yaml.dump(self.config, file)