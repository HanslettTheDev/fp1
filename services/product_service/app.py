import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes import product_bp

app = Flask(__name__)
db = SQLAlchemy() 

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI", "sqlite:///product_service.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(product_bp, url_prefix='/products')
db.init_app(app)

def register_with_consul():
    try:
        import consul
        c = consul.Consul(host='consul', port=8500)
        service_id = "product-service-1"
        c.agent.service.register("product-service", service_id=service_id, address="product_service", port=5001)
        print("Product Service registered with Consul")
    except Exception as e:
        print("Consul registration failed:", e)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    register_with_consul()
    app.run(host='0.0.0.0', port=5001)
