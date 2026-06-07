from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

services = [
    {
        "title": "Airport Pickup",
        "description": "Safe airport pickup and drop service",
        "image": ""
    }
]

cars = [
    {
        "name": "Toyota Innova",
        "type": "SUV",
        "image": ""
    }
]

phone = "+911234567890"

@app.route("/")
def home():
    return render_template(
        "index.html",
        services=services,
        cars=cars,
        phone=phone
    )

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "delete_service":
            index = int(request.form.get("index", -1))
            if 0 <= index < len(services):
                services.pop(index)
        elif action == "delete_car":
            index = int(request.form.get("index", -1))
            if 0 <= index < len(cars):
                cars.pop(index)
        elif action == "update_contact":
            new_phone = request.form.get("phone", "").strip()
            if new_phone:
                global phone
                phone = new_phone
        return redirect("/admin")

    return render_template(
        "admin.html",
        services=services,
        cars=cars,
        phone=phone
    )

@app.route("/add-service", methods=["GET", "POST"])
def add_service():

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        image_file = request.files.get("image") or request.files.get("service_image")
        image_filename = ""

        if image_file and image_file.filename:
            image_filename = secure_filename(image_file.filename)
            image_file.save(
                os.path.join(
                    app.config['UPLOAD_FOLDER'],
                    image_filename
                )
            )

        services.append({
            "title": title,
            "description": description,
            "image": image_filename
        })

        return redirect("/admin")

    return render_template("add_service.html")

@app.route("/add-car", methods=["GET", "POST"])
def add_car():

    if request.method == "POST":

        name = request.form["name"]
        car_type = request.form["type"]
        image_file = request.files.get("image") or request.files.get("car_image")
        image_filename = ""

        if image_file and image_file.filename:
            image_filename = secure_filename(image_file.filename)
            image_file.save(
                os.path.join(
                    app.config['UPLOAD_FOLDER'],
                    image_filename
                )
            )

        cars.append({
            "name": name,
            "type": car_type,
            "image": image_filename
        })

        return redirect("/admin")

    return render_template("add_car.html")

if __name__ == "__main__":
    app.run(debug=True)