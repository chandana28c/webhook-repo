from flask import Flask,render_template

from app.webhook.routes import webhook
from app.extensions import mongo


# Creating our flask app
def create_app():
    app = Flask(__name__)

    # MongoDB configuration
    app.config["MONGO_URI"] = "mongodb://localhost:27017/github_events"
    mongo.init_app(app)

    # Root UI route
    @app.route("/")
    def index():
        return render_template("index.html")

    # Register webhook blueprint
    app.register_blueprint(webhook)

    return app
