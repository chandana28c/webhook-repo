from flask import Flask

from app.webhook.routes import webhook


# Creating our flask app
def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/github_events"

    from app.extensions import mongo
    mongo.init_app(app)

    app.register_blueprint(webhook)
    return app
