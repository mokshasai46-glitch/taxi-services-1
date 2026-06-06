from flask import Flask, render_template, request, redirect, abort
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
        "desc": "Safe airport pickup and drop service",
        "image": ""
    }
]

phone = "+911234567890"

cars = [
    {
        "name": "Toyota Innova",
        "type": "SUV",
        "image": ""
    }
]

@app.route("/")
def home():
    return render_template(
        "index.html",
        data={
            "driver_name": "Luxury Driver",
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

            if service_image and service_image.filename:
                filename = secure_filename(service_image.filename)
                service_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                filename = ""

            services.append({
                "title": title,
                "desc": desc,
                "image": filename
            })

        elif action == "delete_service":
            index = int(request.form["index"])
            if 0 <= index < len(services):
                services.pop(index)

        elif action == "add_car":
            name = request.form["car_name"]
            car_type = request.form["car_type"]
            image = request.files.get("car_image")

            if image and image.filename:
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                filename = ""

            cars.append({
                "name": name,
                "type": car_type,
                "image": filename
            })

        elif action == "delete_car":
            index = int(request.form["index"])
            if 0 <= index < len(cars):
                cars.pop(index)

        elif action == "update_contact":
            global phone
            phone = request.form.get("phone", phone)

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

        return redirect("/admin")

    return render_template("add_service.html")

@app.route("/add-car", methods=["GET", "POST"])
def add_car():

    if request.method == "POST":

        name = request.form["name"]
        car_type = request.form["type"]

        image = request.files["image"]

        filename = secure_filename(image.filename)

        image.save(
            os.path.join(
                app.config['UPLOAD_FOLDER'],
                filename
            )
        )

        cars.append({
            "name": name,
            "type": car_type,
            "image": filename
        })

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

        return redirect("/admin")

    return render_template("edit_car.html", car=cars[index], index=index)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
