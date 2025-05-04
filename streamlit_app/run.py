import os
import subprocess

def run_streamlit_app():
    subprocess.run(["streamlit", "run", "main_app.py"])

if __name__ == "__main__":
    run_streamlit_app()
