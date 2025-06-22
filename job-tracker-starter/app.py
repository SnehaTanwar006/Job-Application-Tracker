from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS jobs
                 (id INTEGER PRIMARY KEY, company TEXT, role TEXT, status TEXT, date_applied TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    search_query = request.args.get('q', '')  # get search term from URL

    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()

    if search_query:
        like_query = f"%{search_query}%"
        c.execute("SELECT * FROM jobs WHERE company LIKE ? OR role LIKE ?", (like_query, like_query))
    else:
        c.execute("SELECT * FROM jobs")

    jobs = c.fetchall()
    conn.close()
    return render_template('index.html', jobs=jobs, search_query=search_query)

@app.route('/add', methods=['POST'])
def add():
    company = request.form['company']
    role = request.form['role']
    status = request.form['status']
    date_applied = request.form['date']
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute("INSERT INTO jobs (company, role, status, date_applied) VALUES (?, ?, ?, ?)", 
              (company, role, status, date_applied))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:job_id>')
def delete(job_id):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/edit/<int:job_id>', methods=['GET', 'POST'])
def edit(job_id):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    
    if request.method == 'POST':
        company = request.form['company']
        role = request.form['role']
        status = request.form['status']
        date_applied = request.form['date']
        c.execute("UPDATE jobs SET company = ?, role = ?, status = ?, date_applied = ? WHERE id = ?", 
                  (company, role, status, date_applied, job_id))
        conn.commit()
        conn.close()
        return redirect('/')
    else:
        c.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
        job = c.fetchone()
        conn.close()
        return render_template('edit.html', job=job)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)