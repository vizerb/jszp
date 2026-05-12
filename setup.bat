:: Create virtual environment
python -m venv ./venv

:: Activate virtual environment
call .\venv\Scripts\activate.bat

:: Install requirements
pip install -r requirements.txt

:: Install Playwright dependencies (mainly chromium)
call playwright install chromium

:: Keep the window open after the script finishes
:: pause