from flask import Flask, request, jsonify
import trimesh
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs('uploads', exist_ok=True)

@app.route('/')
def home():
    return '✅ STL Pricing API is live!'

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    mesh = trimesh.load(filepath, file_type='stl')
    volume_cm3 = mesh.volume / 1000  # mm³ to cm³
    weight_g = volume_cm3 * 1.24     # PLA density
    price_inr = weight_g * 4.5 if weight_g > 500 else weight_g * 5

    return jsonify({
        'volume_cm3': round(volume_cm3, 2),
        'weight_g': round(weight_g, 2),
        'price_inr': round(price_inr, 2)
    })

app.run(host='0.0.0.0', port=8080)
