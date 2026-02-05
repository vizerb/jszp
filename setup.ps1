# Create virtual environment
python -m venv ./venv

# Set execution policy
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

# Activate virtual environment
.\venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Install Playwright dependencies (mainly chromium)
playwright install chromium