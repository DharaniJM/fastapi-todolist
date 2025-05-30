
⏱️ FastAPI Time Tracker
            A modern, dark-themed web application to manage and track your daily tasks using FastAPI, PostgreSQL, and Jinja2. This tool lets users add, complete, and delete tasks while visualizing 
            how time is spent across various categories.

🚀 Features 
✅ Add, view, and delete tasks
🕒 Track time spent per task and category
📅 Filter tasks by date range
📊 Visual analysis with clean cards
☑️ Mark tasks as completed with checkboxes
🌙 Dark-themed, responsive UI
🔄 Dynamic homepage updates on reload
🗃️ PostgreSQL integration for data persistence

🛠️ Tech Stack
Backend: FastAPI
Frontend: HTML, CSS (custom dark theme), Jinja2, Js
Database: PostgreSQL
Database Driver: psycopg2
Templating Engine: Jinja2

📁 Project Structure

fastapi-todolist/
│
├── static/               # Static assets (optional)
├── templates/            # Jinja2 HTML templates
├── main.py               # Main FastAPI application
├── database.py           # PostgreSQL connection and queries
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation


💻 Setup Instructions

1. Clone the repository:

git clone https://github.com/DharaniJM/fastapi-todolist.git
cd fastapi-todolist

2. Create and activate virtual environment:


python -m venv venv
venv\Scripts\activate      # On Windows

# OR

source venv/bin/activate   # On macOS/Linux


3. Install dependencies:

pip install -r requirements.txt


4. Set up your PostgreSQL database:

     * Create a database (e.g., task_db)

     * Set your database URL in main.py or via environment variable:


DATABASE_URL = "postgresql://<username>:<password>@localhost/<database_name>"


5. Run the app:

uvicorn main:app --reload


6. Visit the app in your browser:

http://127.0.0.1:8000


🤝 Contributing
Contributions are welcome! Feel free to fork the repo and submit a pull request. For major changes, open an issue first to discuss.

