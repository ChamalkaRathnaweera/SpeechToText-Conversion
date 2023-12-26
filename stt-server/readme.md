# Create a Virtual Environment
python -m venv venv
# On Windows, use: python -m venv venv

# Activate the Virtual Environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# .\venv\Scripts\activate

# Install Dependencies
pip install -r requirements.txt

# Run the Flask App
python app.py

# Visit http://localhost:5000//get_transcript ["GET", "POST"]
pass the audio file as 'file' in body