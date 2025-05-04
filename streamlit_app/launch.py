import subprocess
import webbrowser
import time
import os
import sys

# Récupère le chemin du script
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# Lance Streamlit
script_path = os.path.join(base_path, "run.py")
subprocess.Popen(["streamlit", "run", script_path], shell=True)

# Ouvre le navigateur
time.sleep(2)
webbrowser.open("http://localhost:8501")
