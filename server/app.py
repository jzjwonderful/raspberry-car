from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = "229FFD94-E824-47C4-8193-987BD18CDDED"

@app.route('/')
def index():
    return render_template("remote_car_controller.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0")
