from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import json
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DATA_FILE = 'data.json'

services = []
cars = []
phone = "+911234567890"


def load_data():
    global services, cars, phone
    if not os.path.exists(DATA_FILE):
        save_data()
        return

    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            services = data.get('services', []) or []
            cars = data.get('cars', []) or []
            phone = data.get('phone', phone) or phone
    except (ValueError, IOError):
        services = []
        cars = []
        phone = phone


def save_data():
    data = {
        'services': services,
        'cars': cars,
        'phone': phone
    }
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


load_data()

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
        save_data()
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
        save_data()

        return redirect("/admin")

    return render_template("add_service.html")

@app.route("/add-car", methods=["GET", "POST"])
def add_car():

    if request.method == "POST":

        name = request.form["name"]
        car_type = request.form["type"]
        specification = request.form.get("specification", "").strip()
        rate_per_km = request.form.get("rate_per_km", "").strip()
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

        try:
            rate_per_km_value = float(rate_per_km) if rate_per_km else 0.0
        except ValueError:
            rate_per_km_value = 0.0

        cars.append({
            "name": name,
            "type": car_type,
            "specification": specification,
            "rate_per_km": rate_per_km_value,
            "image": image_filename
        })
        save_data()

        return redirect("/admin")

    return render_template("add_car.html")

@app.route("/edit-car/<int:index>", methods=["GET", "POST"])
def edit_car(index):
    if index < 0 or index >= len(cars):
        return redirect("/admin")

    car = cars[index]

    if request.method == "POST":
        car["name"] = request.form["name"]
        car["type"] = request.form["type"]
        car["specification"] = request.form.get("specification", "").strip()
        rate_per_km = request.form.get("rate_per_km", "").strip()
        image_file = request.files.get("image") or request.files.get("car_image")

        if image_file and image_file.filename:
            image_filename = secure_filename(image_file.filename)
            image_file.save(
                os.path.join(
                    app.config['UPLOAD_FOLDER'],
                    image_filename
                )
            )
            car["image"] = image_filename

        try:
            car["rate_per_km"] = float(rate_per_km) if rate_per_km else car.get("rate_per_km", 0.0)
        except ValueError:
            car["rate_per_km"] = car.get("rate_per_km", 0.0)

        save_data()
        return redirect("/admin")

    return render_template("edit_car.html", car=car)

if __name__ == "__main__":
    app.run(debug=True)