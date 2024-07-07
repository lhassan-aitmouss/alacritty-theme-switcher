# Alacritty Theme Switcher

A desktop app built with Python and PyQt6 to easily change themes in Alacritty, a fast, cross-platform terminal emulator.

## Features

- View list of available Alacritty themes
- Apply selected theme with one click
- Restart Alacritty to see changes

## Requirements

- Python 3.12 or higher
- PyQt6
- PyYAML
- Alacritty installed and set up

## Setup

1. Clone this repo:
git clone https://github.com/your-username/alacritty-theme-switcher.git
cd alacritty-theme-switcher

2. Create and activate a virtual environment:
conda create -n pyqt6 python=3.12 -y
conda activate pyqt6

3. Install dependencies:
pip install -r requirements.txt

## Config

Edit `config.yaml` to set the correct paths for your Alacritty config and themes folder.

## Usage

Run the main script:
python main.py

Choose a theme from the list, click "Apply Theme", then "Restart Alacritty" to see changes.

## Contributing

Contributions welcome! Feel free to open an issue or submit a pull request.

## License

This project is under the MIT License. See the `LICENSE` file for details.
