cat > README.md << 'EOF'
# ⏱️ FastAPI Time Tracker

A modern, dark-themed web application to manage and track your daily tasks using **FastAPI**, **PostgreSQL**, and **Jinja2**.  
Easily add, complete, delete, and analyze your tasks with a smooth, responsive UI and detailed time breakdowns.

---

## 🚀 Features

- ✅ Add, view, and delete tasks  
- 🕒 Track time spent per task and category  
- 📅 Filter tasks by date range  
- 📊 Visual time analysis (cards per category)  
- ☑️ Mark tasks as completed using checkboxes  
- 🌙 Clean dark-themed, responsive interface  
- 🔄 Live updates on homepage reload  
- 🗃️ PostgreSQL integration for persistent storage  

---

## 🛠️ Tech Stack

- **Backend**: FastAPI  
- **Frontend**: HTML, CSS (dark theme), Jinja2, JavaScript  
- **Database**: PostgreSQL  
- **Database Driver**: psycopg2  
- **Templating Engine**: Jinja2  

---

## 📁 Project Structure

\`\`\`
fastapi-todolist/
│
├── static/             # (Optional) Static assets (CSS, images, JS)
├── templates/          # Jinja2 HTML templates
├── main.py             # FastAPI application entry point
├── database.py         # PostgreSQL connection and queries
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
\`\`\`

---

## 💻 Setup Instructions

### 1. Clone the repository

\`\`\`bash
git clone https://github.com/DharaniJM/fastapi-todolist.git
cd fastapi-todolist
\`\`\`

### 2. Create and activate virtual environment

\`\`\`bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
\`\`\`

### 3. Install dependencies

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Set up PostgreSQL

- Create a new PostgreSQL database (e.g., \`task_db\`)
- Update your \`DATABASE_URL\` in \`main.py\` or as an environment variable:

\`\`\`python
DATABASE_URL = "postgresql://<username>:<password>@localhost/task_db"
\`\`\`

### 5. Run the application

\`\`\`bash
uvicorn main:app --reload
\`\`\`

### 6. Visit in browser

\`\`\`
http://127.0.0.1:8000
\`\`\`

---

## 📸 Screenshots

> You can include screenshots like this (after uploading images to the \`images/\` folder):

\`\`\`md
### Homepage
![Homepage](images/homepage.png)

### Time Analysis View
![Analysis](images/analysis.png)
\`\`\`

---

## 🤝 Contributing

Contributions are welcome!  
- Fork the repository  
- Create a new branch  
- Make your changes  
- Submit a pull request  

For major features or bugs, open an issue first to discuss your ideas.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---
EOF
