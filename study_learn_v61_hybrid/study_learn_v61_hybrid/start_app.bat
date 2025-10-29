@echo off
setlocal

REM --- Create venv if not exists ---
if not exist ".venv" (
  py -m venv .venv
)

call .venv\Scripts\activate

REM --- Upgrade pip and install requirements ---
python -m pip install --upgrade pip
pip install -r requirements.txt

REM --- Launch Streamlit ---
set PORT=8501
for /l %%p in (8501,1,8510) do (
  set PORT=%%p
  streamlit run streamlit_app.py --server.port %%p
  if %ERRORLEVEL%==0 goto :end
)

:end
pause
