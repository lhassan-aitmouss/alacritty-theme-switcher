import subprocess

def restart_alacritty():
    subprocess.run(["pkill", "alacritty"])
    subprocess.Popen(["alacritty"])