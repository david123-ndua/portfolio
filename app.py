import sqlite3 as sql
from datetime import datetime
from flask_wtf.csrf import CSRFProtect
import os
from flask_mail import Mail, Message
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)
from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)

from itsdangerous import (
    URLSafeTimedSerializer,
    BadSignature,
    SignatureExpired
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

from db import get_db_connection
load_dotenv()

app = Flask(__name__)

@app.context_processor
def inject_current_year():
    return {
        "current_year": datetime.now().year
    }
    
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

mail = Mail(app)

serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])

app.config["UPLOAD_FOLDER"] = os.path.join(
    BASE_DIR,
    "static",
    "uploads"
)

os.makedirs(
    app.config["UPLOAD_FOLDER"],
    exist_ok=True
)
#==================================================
# LOGIN REQUIRED
#==================================================

from functools import wraps

def login_required(view):

    @wraps(view)
    def wrapped_view(*args, **kwargs):

        if "admin" not in session:

            flash("Please login first.", "warning")

            return redirect(url_for("admin"))

        return view(*args, **kwargs)

    return wrapped_view


@app.route("/")
def index():
    return render_template("index.html", active="home")


@app.route("/about")
def about():
    return render_template("about.html", active="about")

from email_validator import validate_email, EmailNotValidError

@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        # ==========================================
        # GET FORM DATA SAFELY
        # ==========================================

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        subject = request.form.get("subject", "").strip()
        message = request.form.get("message", "").strip()

        # ==========================================
        # REQUIRED FIELDS
        # ==========================================

        if not name or not email or not subject or not message:

            flash(
                "Please fill in all fields.",
                "danger"
            )

            return redirect(url_for("contact"))

        # ==========================================
        # LENGTH LIMITS
        # ==========================================

        if len(name) > 100:

            flash(
                "Name is too long.",
                "danger"
            )

            return redirect(url_for("contact"))

        if len(email) > 150:

            flash(
                "Email address is too long.",
                "danger"
            )

            return redirect(url_for("contact"))

        if len(subject) > 200:

            flash(
                "Subject is too long.",
                "danger"
            )

            return redirect(url_for("contact"))

        if len(message) > 5000:

            flash(
                "Message is too long. Please keep it under 5000 characters.",
                "danger"
            )

            return redirect(url_for("contact"))

        # ==========================================
        # VALIDATE EMAIL
        # ==========================================

        try:

            valid_email = validate_email(email)

            email = valid_email.normalized

        except EmailNotValidError:

            flash(
                "Please enter a valid email address.",
                "danger"
            )

            return redirect(url_for("contact"))

        # ==========================================
        # DATABASE
        # ==========================================

        conn = get_db_connection()

        conn.execute(
            """
            INSERT INTO messages(
                name,
                email,
                subject,
                message
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                name,
                email,
                subject,
                message
            )
        )

        conn.commit()
        conn.close()

        # ==========================================
        # SEND EMAIL NOTIFICATION
        # ==========================================

        msg = Message(
            subject=f"New Portfolio Message: {subject}",
            recipients=[
                "nduadavid8@gmail.com"
            ],
            reply_to=email
        )

        msg.body = f"""
You have received a new message through your portfolio.

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}

--------------------------------
Portfolio Contact System
"""

        mail.send(msg)

        # ==========================================
        # SUCCESS
        # ==========================================

        flash(
            "Your message has been sent successfully!",
            "success"
        )

        return redirect(url_for("contact"))

    return render_template(
        "contact.html"
    )

@app.route("/projects")
def projects():
    # Get all projects from the database
    conn = get_db_connection()
    projects = conn.execute("SELECT * FROM projects ORDER BY created_at DESC").fetchall()
    conn.close()
    return render_template("projects.html", projects=projects)

@app.route("/dashboard")
@login_required
def dashboard():

    conn = get_db_connection()

    total_projects = conn.execute(
        "SELECT COUNT(*) FROM projects"
    ).fetchone()[0]

    # Temporary values until we create the tables
    featured_projects = conn.execute(
    "SELECT COUNT(*) FROM projects WHERE featured = 1"
    ).fetchone()[0]
    
    total_messages = conn.execute(
    "SELECT COUNT(*) FROM messages WHERE is_read = 0"
    ).fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        active="admin",
        total_projects=total_projects,
        featured_projects=featured_projects,
        total_messages=total_messages
    )
    
@app.route("/dashboard/upload-cv", methods=["POST"])
@login_required
def upload_cv():

    file = request.files.get("cv")

    if not file or not file.filename:
        flash("Please select a CV PDF.", "danger")
        return redirect(url_for("dashboard"))

    filename = file.filename

    if not filename.lower().endswith(".pdf"):
        flash("Only PDF files are allowed.", "danger")
        return redirect(url_for("dashboard"))

    filename = "David_CV.pdf"

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(filepath)

    flash("CV uploaded successfully.", "success")

    return redirect(url_for("dashboard"))


@app.route("/dashboard/add-project", methods=["GET", "POST"])
@login_required
def add_project():

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        category = request.form["category"]
        technologies = request.form["technologies"]
        github = request.form["github"]

        image = request.files.get("image")

        filename = ""

        if image is not None and image.filename:
            
            filename = secure_filename(str(image.filename))

            image.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

        conn = get_db_connection()

        conn.execute("""

            INSERT INTO projects(

                title,

                description,

                category,

                technologies,

                github_link,

                image

            )

            VALUES(?,?,?,?,?,?)

        """,(

            title,

            description,

            category,

            technologies,

            github,

            filename

        ))

        conn.commit()

        conn.close()

        flash("Project added successfully.","success")

        return redirect(url_for("manage_projects"))

    return render_template(
        "add_project.html",
        active="admin"
    )
#==================================================
# MANAGE PROJECTS
#==================================================

@app.route("/dashboard/projects")
@login_required
def manage_projects():

    conn = get_db_connection()

    projects = conn.execute("""

        SELECT *

        FROM projects

        ORDER BY id DESC

    """).fetchall()

    conn.close()

    return render_template(

        "manage_projects.html",

        projects=projects,

        active="admin"

    )
    
    # ==================================================
# MANAGE CONTACT MESSAGES
# ==================================================

@app.route("/dashboard/messages")
@login_required
def manage_messages():

    conn = get_db_connection()

    messages = conn.execute("""
        SELECT *
        FROM messages
        ORDER BY created_at DESC
    """).fetchall()

    conn.close()

    return render_template(
        "manage_messages.html",
        messages=messages,
        active="admin"
    )
    
# ==================================================
# TOGGLE MESSAGE READ STATUS
# ==================================================

@app.route("/dashboard/messages/toggle-read/<int:id>")
@login_required
def toggle_message_read(id):

    conn = get_db_connection()

    message = conn.execute(
        "SELECT is_read FROM messages WHERE id=?",
        (id,)
    ).fetchone()

    if message is None:

        conn.close()

        flash("Message not found.", "danger")

        return redirect(url_for("manage_messages"))

    new_status = 0 if message["is_read"] else 1

    conn.execute(
        "UPDATE messages SET is_read=? WHERE id=?",
        (new_status, id)
    )

    conn.commit()
    conn.close()

    flash("Message status updated.", "success")

    return redirect(url_for("manage_messages"))

# ==================================================
# DELETE CONTACT MESSAGE
# ==================================================

@app.route("/dashboard/messages/delete/<int:id>")
@login_required
def delete_message(id):

    conn = get_db_connection()

    message = conn.execute(
        "SELECT id FROM messages WHERE id=?",
        (id,)
    ).fetchone()

    if message is None:

        conn.close()

        flash("Message not found.", "danger")

        return redirect(url_for("manage_messages"))

    conn.execute(
        "DELETE FROM messages WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    flash("Message deleted successfully.", "success")

    return redirect(url_for("manage_messages"))

#======
# ============================================
# EDIT PROJECT
#==================================================

@app.route("/dashboard/edit-project/<int:id>", methods=["GET", "POST"])
@login_required
def edit_project(id):

    conn = get_db_connection()

    project = conn.execute(
        "SELECT * FROM projects WHERE id=?",
        (id,)
    ).fetchone()
    

    if project is None:

        conn.close()

        flash("Project not found.", "danger")

        return redirect(url_for("manage_projects"))

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        category = request.form["category"]
        technologies = request.form["technologies"]
        github = request.form["github"]
    
        
        

        #handle uploads
        image = request.files.get("image")
    
        filename = project["image"]
    
        if image and image.filename:

            filename = secure_filename(str(image.filename))

            image.save(

                os.path.join(

                    app.config["UPLOAD_FOLDER"],

                    filename

                )

            )

        conn.execute("""

            UPDATE projects

            SET

                title=?,

                description=?,

                category=?,

                technologies=?,

                github_link=?,
                
                image=?

            WHERE id=?

        """,
        (

        title,

        description,

        category,

        technologies,

        github,

        filename,

        id

        ))

        conn.commit()

        conn.close()

        flash("Project updated successfully.", "success")

        return redirect(url_for("manage_projects"))

    conn.close()

    return render_template(

        "edit_project.html",

        project=project,

        active="admin"

    )
    
#==================================================
# DELETE PROJECT
#==================================================

@app.route("/dashboard/delete-project/<int:id>")
@login_required
def delete_project(id):

    conn = get_db_connection()

    conn.execute(

        "DELETE FROM projects WHERE id=?",

        (id,)

    )

    conn.commit()

    conn.close()

    flash("Project deleted successfully.","success")
    
    return redirect(url_for("manage_projects"))

#==================================================
# TOGGLE FEATURED
#==================================================

@app.route("/dashboard/toggle-featured/<int:id>")
@login_required
def toggle_featured(id):

    conn = get_db_connection()

    project = conn.execute(
        "SELECT featured FROM projects WHERE id=?",
        (id,)
    ).fetchone()

    if project is None:

        conn.close()

        flash("Project not found.", "danger")

        return redirect(url_for("manage_projects"))

    new_value = 0 if project["featured"] else 1

    conn.execute(
        "UPDATE projects SET featured=? WHERE id=?",
        (new_value, id)
    )

    conn.commit()
    conn.close()

    flash("Featured status updated.", "success")

    return redirect(url_for("manage_projects"))


#==================================================
# CHANGE PASSWORD
#==================================================

@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()

        admin = conn.execute(
            """
            SELECT *
            FROM admins
            WHERE username=?
            """,
            (username,)
        ).fetchone()

        conn.close()

        if admin and check_password_hash(
            admin["password_hash"],
            password
        ):

            session["admin"] = admin["username"]

            flash(
                "Welcome back!",
                "success"
            )

            return redirect(
                url_for("dashboard")
            )

        flash(
            "Invalid username or password.",
            "danger"
        )

    return render_template(
        "admin.html",
        active="admin"
    )
    
@app.route("/dashboard/change-password", methods=["GET", "POST"])
@login_required
def change_password():

    if request.method == "POST":

        current_password = request.form["current_password"]

        new_password = request.form["new_password"]

        confirm_password = request.form["confirm_password"]

        conn = get_db_connection()

        admin = conn.execute(
            "SELECT * FROM admins WHERE username=?",
            (session["admin"],)
        ).fetchone()

        # Check current password
        if not check_password_hash(
            admin["password_hash"],
            current_password
        ):

            conn.close()

            flash("Current password is incorrect.", "danger")

            return redirect(url_for("change_password"))

        # Check matching passwords
        if new_password != confirm_password:

            conn.close()

            flash("New passwords do not match.", "danger")

            return redirect(url_for("change_password"))

        # Update password
        new_hash = generate_password_hash(new_password)

        conn.execute(
            """
            UPDATE admins

            SET password_hash=?

            WHERE id=?
            """,
            (
                new_hash,
                admin["id"]
            )
        )

        conn.commit()

        conn.close()

        flash("Password changed successfully.", "success")

        return redirect(url_for("dashboard"))

    return render_template(
        "change_password.html",
        active="admin"
    )

@app.route("/admin/forgot-password", methods=["GET", "POST"])
def forgot_password():

    if request.method == "POST":

        email = request.form["email"].strip()

        conn = get_db_connection()

        admin = conn.execute(
            """
            SELECT *
            FROM admins
            WHERE email=?
            """,
            (email,)
        ).fetchone()

        conn.close()

        # Always show the same message
        # so we don't reveal whether an email exists.
        if admin:

            token = serializer.dumps(
                email,
                salt="password-reset"
            )

            reset_url = url_for(
                "reset_password",
                token=token,
                _external=True
            )

            msg = Message(
                "Portfolio Admin Password Reset",
                recipients=[email]
            )

            msg.body = f"""
Hello,

A password reset was requested for your Portfolio Admin account.

Click the link below to reset your password:

{reset_url}

This link will expire after 30 minutes.

If you did not request this reset, you can safely ignore this email.

David Kyalo Portfolio
"""

            mail.send(msg)

        flash(
            "If that email belongs to an administrator account, "
            "a password reset link has been sent.",
            "success"
        )

        return redirect(url_for("admin"))

    return render_template(
        "forgot_password.html",
        active="admin"
    )
    
@app.route("/admin/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):

    try:
        email = serializer.loads(
            token,
            salt="password-reset",
            max_age=1800
        )

    except SignatureExpired:
        flash(
            "This password reset link has expired. Please request a new one.",
            "danger"
        )
        return redirect(url_for("forgot_password"))

    except BadSignature:
        flash(
            "This password reset link is invalid.",
            "danger"
        )
        return redirect(url_for("forgot_password"))

    if request.method == "POST":

        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        if new_password != confirm_password:

            flash(
                "Passwords do not match.",
                "danger"
            )

            return redirect(
                url_for(
                    "reset_password",
                    token=token
                )
            )

        if len(new_password) < 8:

            flash(
                "Password must be at least 8 characters long.",
                "danger"
            )

            return redirect(
                url_for(
                    "reset_password",
                    token=token
                )
            )

        new_hash = generate_password_hash(
            new_password
        )

        conn = get_db_connection()

        conn.execute(
            """
            UPDATE admins
            SET password_hash=?
            WHERE email=?
            """,
            (new_hash, email)
        )

        conn.commit()
        conn.close()

        flash(
            "Your password has been reset successfully. You can now log in.",
            "success"
        )

        return redirect(url_for("admin"))

    return render_template(
        "reset_password.html",
        active="admin"
    )
    
@app.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully.", "success")

    return redirect(url_for("admin"))


    
if __name__ == "__main__":
    app.run(debug=True)