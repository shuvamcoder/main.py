from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect('comments.db')
c = conn.cursor()

try:
    c.execute('''CREATE TABLE IF NOT EXISTS comments (id INTEGER PRIMARY KEY, author TEXT, text TEXT)''')
    conn.commit()
except sqlite3.OperationalError as e:
    if 'table comments already exists' in str(e):
        print('Table already exists. Skipping table creation.')
    else:
        raise

@app.route("/")
def home():
    # Fetch comments from the database or any other data source
    conn = sqlite3.connect('comments.db')
    c = conn.cursor()

    c.execute("SELECT * FROM comments")
    rows = c.fetchall()
    conn.close()

    comments = [{'author': row[1], 'text': row[2]} for row in rows]

    return render_template("index.html", comments=comments)

@app.route("/about_me")
def about_me():
    return render_template("about_me.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/books")
def books():
    return render_template("books.html")

@app.route("/book_over")
def book_over():
    return render_template("book_over.html")

@app.route("/book_char")
def video():
    return render_template("video.html")

@app.route("/blog")
def blog():
    return render_template("blog.html")

@app.route("/com", methods=["GET", "POST"])
def com():
    if request.method == "POST":
        author = request.form["name"]
        text = request.form["comment"]

        # Save the comment to the database or any other data source
        conn = sqlite3.connect('comments.db')
        c = conn.cursor()
        c.execute("INSERT INTO comments (author, text) VALUES (?, ?)", (author, text))
        conn.commit()
        conn.close()

        return redirect("/com")  # Redirect to the comments page after submitting the form

    # Fetch comments from the database or any other data source
    conn = sqlite3.connect('comments.db')
    c = conn.cursor()
    c.execute("SELECT * FROM comments ORDER BY id DESC LIMIT 12")
    rows = c.fetchall()
    conn.close()

    comments = [{'author': row[1], 'text': row[2]} for row in rows]

    return render_template("com.html", comments=comments)

@app.route('/delete_comment/<int:id>', methods=['POST'])
def delete_comment(id):
    conn = sqlite3.connect('comments.db')
    c = conn.cursor()
    c.execute("DELETE FROM comments WHERE id = ?", (id))
    conn.commit()
    conn.close()
    return redirect('com.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)