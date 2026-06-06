# Taxi Booking Flask App

This is a Flask-based taxi booking demo with admin and customer pages.

## Deploying online

### Recommended setup
1. Push this repository to GitHub.
2. Use a Python web host such as Heroku, Render, or Railway.

### Heroku
1. Install the Heroku CLI.
2. Run `heroku create`.
3. Run `git push heroku main` (or `master` as appropriate).
4. Use `heroku open` to view the app.

### Render / Railway
1. Create a new Web Service.
2. Connect your GitHub repo.
3. Set the build command to `pip install -r requirements.txt`.
4. Set the start command to `gunicorn app:app`.

## Local run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the app:
   ```bash
   python app.py
   ```
3. Open `http://127.0.0.1:5000`

## Docker

Build the image:
```bash
docker build -t taxi-booking-app .
```

Run the container:
```bash
docker run -p 5000:5000 taxi-booking-app
```

Then open `http://127.0.0.1:5000`

## Docker Compose

Build and start the app with compose:
```bash
docker compose up --build
```

Then open `http://127.0.0.1:5000`

Use `docker compose down` to stop the app.

## Notes

- `app.py` now binds to `0.0.0.0` and listens on the `PORT` environment variable.
- Static uploads are stored in `static/uploads`.
