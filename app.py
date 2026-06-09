from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import json
import os
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DATA_FILE = 'data.json'

services = []
cars = []
phone = "+911234567890"
admin_location = None
admin_address = ""


def load_data():
    global services, cars, phone, admin_location, admin_address
    if not os.path.exists(DATA_FILE):
        save_data()
        return

    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            services = data.get('services', []) or []
            cars = data.get('cars', []) or []
            phone = data.get('phone', phone) or phone
            admin_location = data.get('admin_location') or None
            admin_address = data.get('admin_address', '') or ''
    except (ValueError, IOError):
        services = []
        cars = []
        phone = phone
        admin_location = None
        admin_address = ''


def save_data():
    data = {
        'services': services,
        'cars': cars,
        'phone': phone,
        'admin_location': admin_location,
        'admin_address': admin_address
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
        phone=phone,
        admin_location=admin_location,
        admin_address=admin_address
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
            new_address = request.form.get("address", "").strip()
            if new_phone:
                global phone
                phone = new_phone
            global admin_address
            admin_address = new_address
        save_data()
        return redirect("/admin")

    return render_template(
        "admin.html",
        services=services,
        cars=cars,
        phone=phone,
        admin_location=admin_location,
        admin_address=admin_address
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
        save_data()

        return redirect("/admin")

    return render_template("add_car.html")


@app.route('/update-admin-location', methods=['POST'])
def update_admin_location():
    global admin_location
    data = request.get_json(silent=True)
    if not data:
        return {'success': False, 'error': 'Invalid JSON payload'}, 400

    lat = data.get('lat')
    lon = data.get('lon')
    if lat is None or lon is None:
        return {'success': False, 'error': 'Missing lat/lon'}, 400

    try:
        lat = float(lat)
        lon = float(lon)
    except (TypeError, ValueError):
        return {'success': False, 'error': 'Invalid coordinates'}, 400

    admin_location = {
        'lat': lat,
        'lon': lon,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    save_data()
    return {'success': True, 'admin_location': admin_location}


if __name__ == "__main__":
    app.run(debug=True)