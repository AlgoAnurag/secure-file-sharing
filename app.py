from flask import Flask, request, send_file, jsonify, render_template
import os
from crypto_utils import encrypt_file, decrypt_file

# Initialize Flask app
app = Flask(__name__)

# Folder to store encrypted files
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Route to render the main page
@app.route('/')
def index():
    return render_template('index.html')

# Upload & Encrypt File (Local Storage)
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    file_data = file.read()

    try:
        encrypted_data = encrypt_file(file_data)
        encrypted_filename = os.path.join(UPLOAD_FOLDER, f"{file.filename}.enc")

        # Save encrypted file
        with open(encrypted_filename, "w") as f:
            f.write(encrypted_data)

        return jsonify({'message': 'File uploaded securely!', 'filename': f"{file.filename}.enc"}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Download & Decrypt File (Local Storage)
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    encrypted_file_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(encrypted_file_path):
        return jsonify({'error': 'File not found'}), 404

    try:
        # Read encrypted file
        with open(encrypted_file_path, "r") as f:
            encrypted_data = f.read()

        # Decrypt file
        decrypted_data = decrypt_file(encrypted_data)
        decrypted_filename = encrypted_file_path.replace(".enc", "")

        # Save decrypted file temporarily
        with open(decrypted_filename, 'wb') as f:
            f.write(decrypted_data)

        return send_file(decrypted_filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the Flask server
if __name__ == '__main__':
    app.run(debug=True)
