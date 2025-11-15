"""
Test/Demo configuration for the Flask application.
This uses a test directory instead of the Windows path.
"""
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
from datetime import datetime
from pathlib import Path
import base64
from PIL import Image, ImageEnhance
import io

app = Flask(__name__)
CORS(app)

# Configuration - Using test path for demo
LOCAL_DATA_PATH = '/tmp/test_images'
SERVER_DATA_PATH = os.path.join(os.path.dirname(__file__), 'server_data')
MODIFICATIONS_FILE = os.path.join(os.path.dirname(__file__), 'modifications.json')

# Ensure server data directory exists
os.makedirs(SERVER_DATA_PATH, exist_ok=True)

# Load or initialize modifications history
if os.path.exists(MODIFICATIONS_FILE):
    with open(MODIFICATIONS_FILE, 'r') as f:
        modifications_history = json.load(f)
else:
    modifications_history = {}


def save_modifications():
    """Save modifications history to file."""
    with open(MODIFICATIONS_FILE, 'w') as f:
        json.dump(modifications_history, f, indent=2)


def apply_brightness_to_server_image(image_path, brightness_factor):
    """Apply brightness modification to server's local dataset."""
    try:
        server_image_path = os.path.join(SERVER_DATA_PATH, os.path.basename(image_path))
        
        # If server doesn't have the image yet, create a placeholder
        if not os.path.exists(server_image_path):
            # For demo purposes, we'll note that the server would have this image
            # In production, the server would have its own copy
            return True
        
        # Open the image
        img = Image.open(server_image_path)
        
        # Apply brightness adjustment
        enhancer = ImageEnhance.Brightness(img)
        adjusted_img = enhancer.enhance(brightness_factor)
        
        # Save the adjusted image
        adjusted_img.save(server_image_path)
        return True
    except Exception as e:
        print(f"Error applying brightness to server image: {e}")
        return False


@app.route('/')
def index():
    """Serve the main application page."""
    return render_template('index.html')


@app.route('/api/images')
def list_images():
    """List available images in the local directory."""
    try:
        # Check if local path exists
        if not os.path.exists(LOCAL_DATA_PATH):
            return jsonify({
                'status': 'error',
                'message': f'Local data path does not exist: {LOCAL_DATA_PATH}',
                'images': []
            })
        
        # List image files
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
        images = []
        
        for filename in os.listdir(LOCAL_DATA_PATH):
            ext = os.path.splitext(filename)[1].lower()
            if ext in image_extensions:
                file_path = os.path.join(LOCAL_DATA_PATH, filename)
                images.append({
                    'filename': filename,
                    'path': file_path,
                    'size': os.path.getsize(file_path),
                    'modifications': modifications_history.get(filename, {})
                })
        
        return jsonify({
            'status': 'success',
            'images': images,
            'count': len(images)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'images': []
        })


@app.route('/api/image/<path:filename>')
def get_image(filename):
    """Serve an image file."""
    try:
        return send_from_directory(LOCAL_DATA_PATH, filename)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 404


@app.route('/api/sync_parameters', methods=['POST'])
def sync_parameters():
    """Receive and apply brightness parameters from client."""
    try:
        data = request.json
        image_filename = data.get('filename')
        brightness = data.get('brightness', 1.0)
        timestamp = datetime.now().isoformat()
        
        if not image_filename:
            return jsonify({
                'status': 'error',
                'message': 'Missing filename'
            }), 400
        
        # Store modification parameters
        if image_filename not in modifications_history:
            modifications_history[image_filename] = []
        
        modification_record = {
            'brightness': brightness,
            'timestamp': timestamp,
            'synced': True
        }
        
        modifications_history[image_filename].append(modification_record)
        
        # Apply modifications to server's local dataset
        image_path = os.path.join(LOCAL_DATA_PATH, image_filename)
        server_applied = apply_brightness_to_server_image(image_path, brightness)
        
        # Save modifications history
        save_modifications()
        
        return jsonify({
            'status': 'success',
            'message': 'Parameters synced successfully',
            'filename': image_filename,
            'brightness': brightness,
            'timestamp': timestamp,
            'server_applied': server_applied
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/sync_status')
def sync_status():
    """Get current sync status and modification history."""
    try:
        total_modifications = sum(len(mods) for mods in modifications_history.values())
        
        return jsonify({
            'status': 'success',
            'total_images_modified': len(modifications_history),
            'total_modifications': total_modifications,
            'modifications': modifications_history,
            'server_data_path': SERVER_DATA_PATH,
            'local_data_path': LOCAL_DATA_PATH
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })


@app.route('/api/clear_modifications', methods=['POST'])
def clear_modifications():
    """Clear all modification history."""
    try:
        global modifications_history
        modifications_history = {}
        save_modifications()
        
        return jsonify({
            'status': 'success',
            'message': 'All modifications cleared'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


if __name__ == '__main__':
    print(f"Starting Flask application...")
    print(f"Local data path: {LOCAL_DATA_PATH}")
    print(f"Server data path: {SERVER_DATA_PATH}")
    app.run(debug=True, host='0.0.0.0', port=5000)
