from flask import Flask, render_template, request, redirect, abort
from werkzeug.utils import secure_filename
import json
import os

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024

DATA_FILE = os.path.join(app.root_path, 'data.json')
DEFAULT_DATA = {
    "driver_name": "Luxury Driver",
    "phone": "+911234567890",
    "services": [
        {
            "title": "Airport Pickup",
            "desc": "Safe airport pickup and drop service",
            "image": ""
        }
    ],
    "cars": [
        {
            "name": "Toyota Innova",
            "type": "SUV",
            "image": ""
        }
    ]
}

app.config['JSON_SORT_KEYS'] = False

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_data():
    if not os.path.exists(DATA_FILE):
        return DEFAULT_DATA.copy()

    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (ValueError, OSError):
        return DEFAULT_DATA.copy()


def save_data():
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(
            {
                'driver_name': driver_name,
                'phone': phone,
                'services': services,
                'cars': cars
            },
            f,
            indent=2
        )


data = load_data()

driver_name = data.get('driver_name', DEFAULT_DATA['driver_name'])
phone = data.get('phone', DEFAULT_DATA['phone'])
services = data.get('services', DEFAULT_DATA['services'])
cars = data.get('cars', DEFAULT_DATA['cars'])

save_data()

@app.route("/")
def home():
    return render_template(
        "index.html",
        data={
            "driver_name": driver_name,
            "phone": phone,
            "services": services,
            "cars": cars
        }
    )

@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":
        action = request.form.get("action")

        if action == "add_service":
            title = request.form["service_title"]
            desc = request.form["service_desc"]
            service_image = request.files.get("service_image")

            if service_image and service_image.filename and allowed_file(service_image.filename):
                filename = secure_filename(service_image.filename)
                service_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                filename = ""

            services.append({
                "title": title,
                "desc": desc,
                "image": filename
            })
            save_data()

        elif action == "delete_service":
            try:
                index = int(request.form["index"])
            except (TypeError, ValueError):
                index = -1

            if 0 <= index < len(services):
                services.pop(index)
                save_data()

        elif action == "add_car":
            name = request.form["car_name"]
            car_type = request.form["car_type"]
            image = request.files.get("car_image")

            if image and image.filename and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                filename = ""

            cars.append({
                "name": name,
                "type": car_type,
                "image": filename
            })
            save_data()

        elif action == "delete_car":
            try:
                index = int(request.form["index"])
            except (TypeError, ValueError):
                index = -1

            if 0 <= index < len(cars):
                cars.pop(index)
                save_data()

        elif action == "update_contact":
            global phone
            phone = request.form.get("phone", phone)
            save_data()

        return redirect("/admin")

    return render_template(
        "admin.html",
        data={
            "services": services,
            "cars": cars,
            "phone": phone
        },
        services=services,
        cars=cars,
        phone=phone
    )

@app.route("/add-service", methods=["GET", "POST"])
def add_service():

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]

        services.append({
            "title": title,
            "desc": description
        })
        save_data()

        return redirect("/admin")

    return render_template("add_service.html")

@app.route("/add-car", methods=["GET", "POST"])
def add_car():

    if request.method == "POST":

        name = request.form["name"]
        car_type = request.form["type"]
        image = request.files.get("image")
        filename = ""

        if image and image.filename and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        cars.append({
            "name": name,
            "type": car_type,
            "image": filename
        })
        save_data()

        return redirect("/admin")

    return render_template("add_car.html")

@app.route("/edit-car/<int:index>", methods=["GET", "POST"])
def edit_car(index):

    if index < 0 or index >= len(cars):
        abort(404)

    if request.method == "POST":

        name = request.form["name"]
        car_type = request.form["type"]
        image = request.files.get("image")

        if image and image.filename:
            filename = secure_filename(image.filename)
            image.save(
                os.path.join(
                    app.config['UPLOAD_FOLDER'],
                    filename
                )
            )
        else:
            filename = cars[index]["image"]

        cars[index] = {
            "name": name,
            "type": car_type,
            "image": filename
        }
        save_data()

        return redirect("/admin")

    return render_template("edit_car.html", car=cars[index], index=index)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
