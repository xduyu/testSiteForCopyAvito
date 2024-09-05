from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

DATA_FILE = 'announcements.json'
BLOCKED_IPS_FILE = 'blocked_ips.json'

# Создайте директорию, если её не существует
if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/supersecretdomainfortestDHSACVjdafcsaasdasdajdasdasjdasdasjdasdasdijjasdasdjlaksdljaskdjaskd')
def admin_panel():
    return send_from_directory('', 'supersecretdomainfortestDHSACVjdafcsaasdasdajdasdasjdasdasjdasdasdijjasdasdjlaksdljaskdjaskd.html')

@app.route('/announcements', methods=['POST'])
def add_announcement():
    try:
        ip_address = request.headers.get('X-Forwarded-For') or request.remote_addr
        if is_ip_blocked(ip_address):
            return jsonify({"error": "You are blocked from creating announcements."}), 403
        
        title = request.form.get('title')
        content = request.form.get('content')
        name = request.form.get('name')
        contact = request.form.get('contact')
        image = request.files.get('image')

        if not title or not content:
            return jsonify({"error": "Title and content are required"}), 400

        announcements = []
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as file:
                announcements = json.load(file)

        new_id = max([ann['id'] for ann in announcements], default=0) + 1
        image_path = None
        if image:
            image_filename = f"image_{new_id}.jpg"
            image_path = os.path.join('static', image_filename)
            image.save(image_path)

        new_announcement = {
            'id': new_id,
            'title': title,
            'content': content,
            'name': name,
            'contact': contact,
            'image': image_path
        }

        announcements.append(new_announcement)

        with open(DATA_FILE, 'w') as file:
            json.dump(announcements, file, indent=4)

        return jsonify(new_announcement), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/announcements', methods=['GET'])
def get_announcements():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as file:
                announcements = json.load(file)
            return jsonify(announcements), 200
        else:
            return jsonify([]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/announcements/<int:id>', methods=['GET'])
def get_announcement(id):
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as file:
                announcements = json.load(file)
            announcement = next((ann for ann in announcements if ann['id'] == id), None)
            if announcement:
                return jsonify(announcement), 200
            else:
                return jsonify({"error": "Announcement not found"}), 404
        else:
            return jsonify({"error": "No announcements found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/announcements/<int:id>', methods=['PUT'])
def update_announcement(id):
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as file:
                announcements = json.load(file)
            
            updated_announcements = []
            announcement_found = False
            for ann in announcements:
                if ann['id'] == id:
                    announcement_found = True
                    ann.update({
                        'title': request.form.get('title', ann['title']),
                        'content': request.form.get('content', ann['content']),
                        'name': request.form.get('name', ann['name']),
                        'contact': request.form.get('contact', ann['contact'])
                    })
                    if 'image' in request.files:
                        image_file = request.files['image']
                        if image_file:
                            filename = f"static/{image_file.filename}"
                            image_file.save(filename)
                            ann['image'] = filename
                updated_announcements.append(ann)

            if announcement_found:
                with open(DATA_FILE, 'w') as file:
                    json.dump(updated_announcements, file, indent=4)
                return jsonify({"success": True}), 200
            else:
                return jsonify({"error": "Announcement not found"}), 404
        else:
            return jsonify({"error": "No announcements found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/announcements/<int:id>', methods=['DELETE'])
def delete_announcement(id):
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as file:
                announcements = json.load(file)
            
            new_announcements = [ann for ann in announcements if ann['id'] != id]
            if len(new_announcements) < len(announcements):
                with open(DATA_FILE, 'w') as file:
                    json.dump(new_announcements, file, indent=4)
                return jsonify({"success": True}), 200
            else:
                return jsonify({"error": "Announcement not found"}), 404
        else:
            return jsonify({"error": "No announcements found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/blocked-ips', methods=['POST'])
def block_ip():
    try:
        ip = request.json.get('ip')
        if not ip:
            return jsonify({"error": "IP address is required"}), 400
        
        blocked_ips = load_blocked_ips()
        blocked_ips.add(ip)
        save_blocked_ips(blocked_ips)

        return jsonify({"message": "IP blocked successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/blocked-ips', methods=['GET'])
def get_blocked_ips():
    try:
        blocked_ips = load_blocked_ips()
        return jsonify(list(blocked_ips)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def load_blocked_ips():
    if os.path.exists(BLOCKED_IPS_FILE):
        with open(BLOCKED_IPS_FILE, 'r') as file:
            return set(json.load(file))
    return set()

def save_blocked_ips(blocked_ips):
    with open(BLOCKED_IPS_FILE, 'w') as file:
        json.dump(list(blocked_ips), file)

def is_ip_blocked(ip_address):
    blocked_ips = load_blocked_ips()
    return ip_address in blocked_ips

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')  # Run on all network interfaces
