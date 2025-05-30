import time
from datetime import datetime

import psycopg2
from psycopg2.extras import RealDictCursor

from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.add_middleware(SessionMiddleware, secret_key="1234")
# Connect to PostgreSQL database
while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="db1",
            user="postgres",
            password="5432",  # your actual password here
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("✅ Database connected successfully.")
        break
    except Exception as error:
        print("Database connection failed:", error)
        time.sleep(3)

# Route for homepage (root)
@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


 
@app.get("/login.html", response_class=HTMLResponse)
def homepage(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/return-homepage", response_class=HTMLResponse)
def homepage(request: Request):
   return RedirectResponse(url="/homepage.html", status_code=303)


@app.get("/Analysis-page", response_class=HTMLResponse)
def homepage(request: Request):
    return templates.TemplateResponse("Analysis_page.html", {"request": request})

@app.post("/signup.html", response_class=HTMLResponse)
def signup(
    request: Request,
    email: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    confirm: str = Form(...)
):
    if password != confirm:
        return templates.TemplateResponse("signup.html", {
            "request": request,
            "status": "Passwords do not match!"
        })

    try:
        # Check if user already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            return templates.TemplateResponse("signup.html", {
                "request": request,
                "status": "Email already exists!"
            })

        # Insert plain-text password (not secure, but you requested this)
        cursor.execute(
            "INSERT INTO users (email, password, username) VALUES (%s, %s, %s)",
            (email, password, username)
        )
        conn.commit()
        return templates.TemplateResponse("login.html", {
            "request": request,
            "status": "Account created! Please log in."
        })

    except Exception as e:
        print("Signup error:", e)
        return templates.TemplateResponse("signup.html", {
            "request": request,
            "status": "Server error. Try again later."
        })
    

from fastapi.responses import JSONResponse

@app.post("/update-status")
async def update_status(request: Request):
    try:
        data = await request.json()
        print("Incoming JSON:", data)  # 👈 Add this line

        task_id = data.get("id")
        new_status = data.get("status")

        if not task_id or not new_status:
            print("Missing 'id' or 'status' in request")
            return JSONResponse(status_code=400, content={"error": "Missing id or status"})

        # Update DB
        update_query = "UPDATE tasks SET status = %s WHERE task_id = %s"
        cursor.execute(update_query, (new_status, task_id))
        conn.commit()

        return JSONResponse(content={"success": True})
    except Exception as e:
        print("Error updating status:", e)
        return JSONResponse(status_code=500, content={"error": "Server error"})

    
# Handle login form submission (POST)
@app.post("/login.html", response_class=HTMLResponse)
def login(request: Request, email: str = Form(...), password: str = Form(...)):
    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user is None:
            print("Email not found:", email)
            return templates.TemplateResponse("login.html", {"request": request})

        if user["password"] == password:
            print("Login successful for:", email)
            request.session["user_id"] = user["user_id"] 
            user_id=user["user_id"] 
            user_name=user['username'] # ✅ Save in session
            date = datetime.today().strftime("%Y-%m-%d")

            cursor.execute("""UPDATE tasks SET status = 'missed' WHERE date = CURRENT_DATE AND end_time < CURRENT_TIME AND status IN ('pending') AND user_id = %s""", (user_id,))
            conn.commit()
            cursor.execute("SELECT * FROM tasks WHERE date = %s AND user_id = %s AND status=%s ORDER BY start_time ASC",(date, user_id,"pending"))
            pending_tasks = cursor.fetchall()

# Query 2: Completed + missed tasks
            cursor.execute("SELECT * FROM tasks WHERE date = %s AND user_id = %s AND status IN ('completed', 'missed') ORDER BY start_time ASC",(date, user_id))
            done_tasks = cursor.fetchall()

# Combine both lists: pending tasks first, then done tasks
            records = pending_tasks + done_tasks
            conn.commit()

            cursor.execute("SELECT count(*) FROM tasks WHERE date = %s AND user_id = %s AND status IN ('completed')",(date, user_id))
            no_of_completed = cursor.fetchone()

            cursor.execute("SELECT count(*) FROM tasks WHERE date = %s AND user_id = %s AND status IN ('missed')",(date, user_id))
            no_of_missed = cursor.fetchone()

            cursor.execute("SELECT count(*) FROM tasks WHERE date = %s AND user_id = %s AND status IN ('pending')",(date, user_id))
            no_of_pending = cursor.fetchone()


            cursor.execute("""SELECT category, SUM(EXTRACT(EPOCH FROM (end_time - start_time)) / 60) AS total_minutes FROM tasks WHERE date = %s AND user_id = %s AND status IN ('completed') GROUP BY category  """,(date, user_id))
            category_times = cursor.fetchall()

            
            return templates.TemplateResponse("homepage.html", {
                "request": request, "posts": records , 
                "user_name":user["username"],
                "no_of_completed":no_of_completed,
                "no_of_missed":no_of_missed,
                "no_of_pending":no_of_pending,
                "category_times":category_times,
               "selected_date": date, "user_name":user_name
                })
        else:
            print("Incorrect password for:", email)
            return templates.TemplateResponse("login.html", {"request": request})
    except Exception as e:
        print("Login error:", e)
        return templates.TemplateResponse("login.html", {"request": request})
    

#=================================================================================================================

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, request: Request):
    user_id = request.session.get("user_id")
    print("\n\n\n\n\n\n\taskid",task_id,"\n\n\n\n")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        with conn.cursor() as cursor:
            # Delete task only if it belongs to the logged-in user
            cursor.execute("""
                DELETE FROM tasks WHERE task_id = %s AND user_id = %s
            """, (task_id, user_id))
            if cursor.rowcount == 0:
                return JSONResponse(status_code=404, content={"detail": "Task not found or unauthorized"})
            conn.commit()

        return {"detail": "Task deleted successfully"}

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Error deleting task: {str(e)}"})

@app.post("/Analysis_page.html", response_class=HTMLResponse)
async def analyze_time(
    request: Request,
    from_date: str = Form(...),
    to_date: str = Form(...)
):
    # TEMP hardcoded for testing
    user_id = request.session.get("user_id")

   
    try:
        from_dt = datetime.strptime(from_date, "%Y-%m-%d").date()
        to_dt = datetime.strptime(to_date, "%Y-%m-%d").date()
       
        if from_dt > to_dt:
         
            return templates.TemplateResponse("Analysis_page.html", {
                "request": request,
                "error": "From date must be before or equal to To date",
                "category_data": [],
                "from_date": from_date,
                "to_date": to_date
            })
        
       

        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT category,
                       SUM(EXTRACT(EPOCH FROM (end_time - start_time)) / 60) AS total_minutes
                FROM tasks
                WHERE date BETWEEN %s AND %s
                  AND user_id = %s
                  AND status = 'completed'
                GROUP BY category
                ORDER BY total_minutes DESC
            """, (from_dt, to_dt, user_id))
            rows = cursor.fetchall()
        
        category_data = rows
        


       
        return templates.TemplateResponse("Analysis_page.html", {
            "request": request,
            "category_data": category_data,
            "from_date": from_date,
            "to_date": to_date,
            "error": None
        })

    except Exception as e:
        
        return templates.TemplateResponse("Analysis_page.html", {
            "request": request,
            "category_data": [],
            "error": str(e),
            "from_date": from_date,
            "to_date": to_date
        })

@app.get("/homepage.html", response_class=HTMLResponse)
def homepage_alias(request: Request, date: str = None):
    user_id = request.session.get("user_id")
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    if date is None:
        date = datetime.today().strftime("%Y-%m-%d")

    try:
        # Query 1: Pending tasks only (status NOT in completed or missed)
        cursor.execute("""UPDATE tasks SET status = 'missed' WHERE date = CURRENT_DATE AND end_time < CURRENT_TIME AND status IN ('pending') AND user_id = %s""", (user_id,))
        conn.commit()
        cursor.execute(
        "SELECT * FROM tasks WHERE date = %s AND user_id = %s AND status=%s ORDER BY start_time ASC",
        (date, user_id,"pending")
        )
        pending_tasks = cursor.fetchall()

# Query 2: Completed + missed tasks
        cursor.execute(
        "SELECT * FROM tasks WHERE date = %s AND user_id = %s AND status IN ('completed', 'missed') ORDER BY start_time ASC",
        (date, user_id)
    )
        done_tasks = cursor.fetchall()

# Combine both lists: pending tasks first, then done tasks
        records = pending_tasks + done_tasks
        conn.commit()

        cursor.execute(
        "SELECT count(*) FROM tasks WHERE date = %s AND user_id = %s AND status IN ('completed')",
        (date, user_id)
    )
        no_of_completed = cursor.fetchone()

        cursor.execute(
        "SELECT count(*) FROM tasks WHERE date = %s AND user_id = %s AND status IN ('missed')",
        (date, user_id)
    )
        no_of_missed = cursor.fetchone()

        cursor.execute(
        "SELECT count(*) FROM tasks WHERE date = %s AND user_id = %s AND status IN ('pending')",
        (date, user_id)
    )
        no_of_pending = cursor.fetchone()


        cursor.execute("""SELECT category, SUM(EXTRACT(EPOCH FROM (end_time - start_time)) / 60) AS total_minutes FROM tasks WHERE date = %s AND user_id = %s AND status IN ('completed') GROUP BY category  """,(date, user_id))
        category_times = cursor.fetchall()

    except Exception as e:
        print("Error fetching tasks:", e)
        records = []

    
    return templates.TemplateResponse("homepage.html", {
        "request": request,
        "posts": records,
       
        "no_of_completed":no_of_completed,
        "no_of_missed":no_of_missed,
        "no_of_pending":no_of_pending,
        "category_times":category_times,
        "selected_date": date, "user_name":user["username"]
    })

@app.get("/reload-page", response_class=HTMLResponse)
def task_page(request: Request):
    user_id = request.session.get("user_id")
    cursor.execute("""UPDATE tasks SET status = 'missed' WHERE date = CURRENT_DATE AND end_time < CURRENT_TIME AND status IN ('pending') AND user_id = %s""", (user_id,))
    return RedirectResponse(url="/homepage.html", status_code=303)
# Route for task add page
@app.get("/taskaddpage.html", response_class=HTMLResponse)
def task_page(request: Request):
    return templates.TemplateResponse("taskaddpage.html", {"request": request})

@app.post("/update-status")
async def update_status(request: Request):
    try:
        data = await request.json()
        task_id = data.get("id")
        new_status = data.get("status")

        if not task_id or not new_status:
            return JSONResponse(status_code=400, content={"error": "Missing id or status"})

        update_query = "UPDATE tasks SET status = %s WHERE id = %s"
        cursor.execute(update_query, (new_status, task_id))
        conn.commit()

        return JSONResponse(content={"success": True})

    except Exception as e:
        print("Error updating status:", e)
        return JSONResponse(status_code=500, content={"error": "Server error"})

# Route for task data getting from front end
@app.post("/taskaddpage.html", response_class=HTMLResponse)
def create_task(
    request: Request,
    title: str = Form(...),
    category: str = Form(...),
    description: str = Form(...),
    start_time: str = Form(...),
    end_time: str = Form(...),
    date: str = Form(...)
):
    user_id = request.session.get("user_id")
    try:
        cursor.execute("""
            INSERT INTO tasks (user_id, title, category, description, start_time, end_time, date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            user_id,  # Replace with the actual user_id if available
            title,
            category,
            description,
            start_time,
            end_time,
            date
        ))
        conn.commit()
    except Exception as e:
        print("Database error:", e)
        return HTMLResponse(content=f"Error: {str(e)}", status_code=500)

    return RedirectResponse(url="/homepage.html", status_code=303)