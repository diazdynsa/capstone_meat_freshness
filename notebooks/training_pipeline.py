# ==============================================================================
# SCRIPT TRAINING MODEL KLAFIKASI KESEGARAN DAGING (CAPSTONE PROJECT)
# Salin baris-baris ini ke dalam cell Jupyter Notebook (.ipynb) Anda.
# ==============================================================================

# 1. IMPORT LIBRARY
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2, VGG16
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt
import os

# 2. SETUP DATASET & AUGMENTASI
# Memastikan path dataset selalu valid dari mana pun script di-run
base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'dataset')
train_dir = os.path.join(base_dir, 'train')
val_dir = os.path.join(base_dir, 'val')

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

val_datagen = ImageDataGenerator(rescale=1./255)

print("Memuat dataset training...")
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)

print("Memuat dataset validasi...")
val_generator = val_datagen.flow_from_directory(
    val_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)

# 3. MEMBANGUN MODEL 1: MOBILENETV2 (Baseline)
print("\n=== Membangun Arsitektur MobileNetV2 ===")
base_model_1 = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
for layer in base_model_1.layers:
    layer.trainable = False # Freeze weights pre-trained

x1 = base_model_1.output
x1 = GlobalAveragePooling2D()(x1)
x1 = Dense(128, activation='relu')(x1)
x1 = Dropout(0.5)(x1)
predictions_1 = Dense(3, activation='softmax')(x1) # 3 Kelas: Fresh, Half-Fresh, Spoiled

model_mobilenet = Model(inputs=base_model_1.input, outputs=predictions_1)
model_mobilenet.compile(optimizer=Adam(learning_rate=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])

# 4. TRAINING MODEL MOBILENETV2
print("Mulai Training MobileNetV2...")
history_mobilenet = model_mobilenet.fit(
    train_generator,
    epochs=10,
    validation_data=val_generator
)

# 5. MEMBANGUN MODEL 2: VGG16 (Untuk Perbandingan)
print("\n=== Membangun Arsitektur VGG16 ===")
base_model_2 = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
for layer in base_model_2.layers:
    layer.trainable = False

x2 = base_model_2.output
x2 = GlobalAveragePooling2D()(x2)
x2 = Dense(128, activation='relu')(x2)
x2 = Dropout(0.5)(x2)
predictions_2 = Dense(3, activation='softmax')(x2)

model_vgg = Model(inputs=base_model_2.input, outputs=predictions_2)
model_vgg.compile(optimizer=Adam(learning_rate=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])

# 6. TRAINING MODEL VGG16
print("Mulai Training VGG16...")
history_vgg = model_vgg.fit(
    train_generator,
    epochs=10,
    validation_data=val_generator
)

# 7. EVALUASI DAN VISUALISASI PERBANDINGAN
def plot_comparison(hist1, hist2, title):
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(hist1.history['val_accuracy'], label='MobileNetV2 Val Acc')
    plt.plot(hist2.history['val_accuracy'], label='VGG16 Val Acc')
    plt.title('Perbandingan Validasi Akurasi')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(hist1.history['val_loss'], label='MobileNetV2 Val Loss')
    plt.plot(hist2.history['val_loss'], label='VGG16 Val Loss')
    plt.title('Perbandingan Validasi Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

print("\nMenampilkan grafik perbandingan...")
plot_comparison(history_mobilenet, history_vgg, "Perbandingan MobileNetV2 vs VGG16")

# 8. SIMPAN MODEL TERBAIK
# Asumsi MobileNetV2 lebih efisien dan akurasinya mirip/lebih baik:
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models', 'best_model.h5')
model_mobilenet.save(model_path)
print(f"\nTraining selesai! Model terbaik berhasil disimpan di {model_path}")
