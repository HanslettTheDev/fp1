from flask import Flask
from routes import notification_bp

app = Flask(__name__)
app.register_blueprint(notification_bp, url_prefix='/notifications')

def register_with_consul():
    try:
        import consul
        c = consul.Consul(host='consul', port=8500)
        service_id = "notification-service-1"
        c.agent.service.register("notification-service", service_id=service_id, address="notification_service", port=5003)
        print("Notification Service registered with Consul")
    except Exception as e:
        print("Consul registration failed:", e)

if __name__ == '__main__':
    register_with_consul()
    app.run(host='0.0.0.0', port=5003)
