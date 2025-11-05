from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
#test
app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for flash messages

# MongoDB Atlas connection (replace <username>, <password>, <cluster>, <dbname>)
MONGO_URI = "mongodb+srv://maqs_db_user:UzwPnTZi2Jjf2M8y@cluster0.b3gn9jq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGO_URI)
db = client["test_db"]            # Database name
collection = db["users"]          # Collection nameError: bad auth : authentication failed, full error: {'ok': 0, 'errmsg': 'bad auth : authentication failed', 'code': 8000, 'codeName': 'AtlasError'}

@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        try:
            name = request.form.get("name")
            email = request.form.get("email")

            if not name or not email:
                flash("Both Name and Email are required!", "error")
                return render_template("form.html")

            data = {"name": name, "email": email}
            collection.insert_one(data)
            return redirect(url_for("success"))

        except Exception as e:
            flash(f"Error: {str(e)}", "error")
            return render_template("form.html")

    return render_template("form.html")

@app.route("/success")
def success():
    return render_template("success.html")


# --- View Data Page ---
@app.route("/view")
def view_data():
    try:
        users = list(collection.find())
        return render_template("view.html", users=users)
    except Exception as e:
        return f"<h3>Error loading data: {e}</h3>"




if __name__ == "__main__":
    app.run(debug=True)
