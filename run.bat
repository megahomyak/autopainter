@ECHO OFF
if not exist .installed (
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
echo yes > .installed
)
.\venv\Scripts\python.exe script.py
