import os
import numpy as np
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
import tensorflow as tf
from PIL import Image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB 

# Pastikan folder uploads ada
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Global variable for model
model = None
MODEL_PATH = 'models/best_model.h5' # Sesuaikan dgn model terbaik 

# Label berdasarkan dataset
CLASS_LABELS = ['Fresh', 'Half-Fresh', 'Spoiled']

def load_prediction_model():
    global model
    if os.path.exists(MODEL_PATH):
        try:
            model = tf.keras.models.load_model(MODEL_PATH)
            print("Model berhasil dimuat.")
        except Exception as e:
            print(f"Error memuat model: {e}")
    else:
        print(f"Warning: Model tidak ditemukan di {MODEL_PATH}. Mode mock prediction diaktifkan untuk testing UI.")

def preprocess_image(image_path):
    img = Image.open(image_path).convert('RGB')
    img = img.resize((224, 224)) # Sesuai input MobileNetV2 / VGG16
    img_array = np.array(img) / 255.0 # Normalisasi
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'Tidak ada file yang diunggah'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nama file kosong'})
        
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Jika model belum ada, gunakan mock response untuk mengetes UI
        if model is None:
            import random
            import time
            time.sleep(1.5) # Simulasi waktu komputasi
            predicted_class = random.choice(CLASS_LABELS)
            confidence = round(random.uniform(70.0, 99.9), 2)
            return jsonify({
                'class': predicted_class,
                'confidence': confidence,
                'image_url': f"/{filepath}"
            })
            
        try:
            # Prediksi menggunakan model asli
            processed_img = preprocess_image(filepath)
            predictions = model.predict(processed_img)
            class_idx = np.argmax(predictions[0])
            confidence = round(float(np.max(predictions[0])) * 100, 2)
            
            predicted_class = CLASS_LABELS[class_idx]
            
            return jsonify({
                'class': predicted_class,
                'confidence': confidence,
                'image_url': f"/{filepath}"
            })
        except Exception as e:
            return jsonify({'error': str(e)})

if __name__ == '__main__':
    load_prediction_model()
    app.run(debug=True, port=5000)
