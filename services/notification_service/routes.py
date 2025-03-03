from flask import Blueprint, request, jsonify

notification_bp = Blueprint('notification_bp', __name__)

@notification_bp.route('/send', methods=['POST'])
def send_notification():
    data = request.get_json()
    notif_type = data.get("type")       # "email" or "sms"
    recipient = data.get("recipient")
    message = data.get("message")
    
    if not (notif_type and recipient and message):
        return jsonify({"message": "Missing notification data"}), 400

    # Simulate sending a notification.
    print(f"Sending {notif_type} notification to {recipient}: {message}")
    return jsonify({"message": f"{notif_type.capitalize()} notification sent to {recipient}"}), 201
