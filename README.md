🧠 MindSpace – Mood Tracker & Journal Web App
Welcome to MindSpace, a beautifully simple web app designed to help users track their emotions, reflect on daily moods, and explore mental clarity through journaling. This project was developed as the final submission for the Intro to Web Programming course.

🌐 Live Demo (Optional)
You can include a link here if you deploy the app (e.g., via Render, Replit, or your own server).

📁 Repository Structure
This repository includes:

app.py – main Flask backend

templates/ – all Jinja2 HTML templates

static/css/style.css – core styling

config.py – configuration (SQLite path, etc.)

README.md – this file

GitHub repo: Final-project-Intro-to-Web

💡 Features
✅ User registration & login with session management

✅ Track mood entries by date, mood, intensity, notes, and tags

✅ View mood history in a dashboard

✅ Chart mood trends over time using Chart.js

✅ Filter entries by date, mood, and tags

✅ Export data as CSV

✅ Responsive and theme-toggle UI

✅ Flash messages and route protection for better UX

🛠 Technologies Used
Backend: Python 3, Flask, SQLite, SQLAlchemy

Frontend: HTML5, CSS3, JavaScript, Jinja2, Chart.js

Authentication: Session-based with hashed passwords (Werkzeug)

📦 Setup Instructions
Clone the repo

bash
Copy
Edit
git clone https://github.com/maqsudov-r-auca-2023/Final-project-Intro-to-Web.git
cd Final-project-Intro-to-Web
Create virtual environment

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Run the app

bash
Copy
Edit
python app.py
Visit in browser
Open http://127.0.0.1:5000

🔧 Dependencies
Flask

Flask SQLAlchemy

Werkzeug

Chart.js (via CDN)

You can install all Python dependencies via:

bash
Copy
Edit
pip install flask flask_sqlalchemy werkzeug
✨ Bonus Features
Dark/light theme toggle ☀️🌙

Responsive design for mobile use 📱

Flash messages for all major actions

Tags system for filtering moods by context (#work, #health, etc.)

🚀 Future Improvements
🔐 Per-user mood entry visibility

📊 Advanced analytics and insights

☁️ Cloud deployment (e.g., Render or Heroku)

🧠 AI mood prediction based on notes

📲 REST API for mobile client sync

📌 Submission Checklist
 Python + Flask backend ✅

 SQLite as DB ✅

 HTML, CSS, JS frontend ✅

 At least 1 user interaction (full CRUD + login/logout) ✅

 Code is modular and clean ✅

 Setup, feature list, and instructions ✅

 GitHub repo submitted ✅

Made with 🧠 and 💜 by Rahmonbek Maqsudov
American University of Central Asia – Spring 2025