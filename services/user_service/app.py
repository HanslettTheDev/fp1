from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db
from routes import user_bp
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI", "sqlite:///user_service.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(user_bp, url_prefix='/users')

db = SQLAlchemy()
db.init_app(app)

# Optional: register with Consul for service discovery
def register_with_consul():
    try:
        import consul
        c = consul.Consul(host='consul', port=8500)
        service_id = "user-service-1"
        c.agent.service.register("user-service", service_id=service_id, address="user_service", port=5000)
        print("User Service registered with Consul")
    except Exception as e:
        print("Consul registration failed:", e)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    register_with_consul()
    app.run(host='0.0.0.0', port=5000)
