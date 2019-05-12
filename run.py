from flask import Flask, redirect
import redis
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


redis_url = os.environ.get("REDIS_URL", "redis://redis_cache:6379")
redis = redis.StrictRedis(socket_connect_timeout=3).from_url(redis_url)


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    @app.route("/")
    def get():
        return redirect("/api/docs", code=301)

    from app import api_bp

    app.register_blueprint(api_bp, url_prefix="/api")

    from models import db

    db.init_app(app)

    return app


if __name__ == "__main__":
    app = create_app("config")
    app.run(host="0.0.0.0", debug=True)
