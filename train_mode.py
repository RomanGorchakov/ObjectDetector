import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models, optimizers, metrics
import tensorflow as tf

# Пути к данным
availability_dir = 'images_resized/availability'
absence_dir = 'images_resized/absence'
report_dir = 'report'

os.makedirs(report_dir, exist_ok=True)
os.makedirs('model', exist_ok=True)

# Загрузка изображений
def load_images_from_folder(folder, label):
    images, labels, filenames = [], [], []

    for filename in os.listdir(folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            path = os.path.join(folder, filename)

            img = load_img(path, target_size=(224, 224))
            img_array = img_to_array(img) / 255.0

            images.append(img_array)
            labels.append(label)
            filenames.append(filename)

    return np.array(images), np.array(labels), filenames

# Загрузка данных
availability_images, availability_labels, availability_files = load_images_from_folder(availability_dir, 1)
absence_images, absence_labels, absence_files = load_images_from_folder(absence_dir, 0)

images = np.concatenate([availability_images, absence_images])
labels = np.concatenate([availability_labels, absence_labels])
filenames = availability_files + absence_files

# Разделение данных
X_train, X_temp, y_train, y_temp, f_train, f_temp = train_test_split(
    images, labels, filenames, test_size=0.4, random_state=42)

X_val, X_test, y_val, y_test, f_val, f_test = train_test_split(
    X_temp, y_temp, f_temp, test_size=0.5, random_state=42)

# Аугментация
train_datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True
)

val_datagen = ImageDataGenerator()

# Модель
def build_model():
    base_model = MobileNetV2(
        weights='imagenet',
        include_top=False,
        input_shape=(224, 224, 3)
    )

    base_model.trainable = True

    # Замораживаем часть слоев
    for layer in base_model.layers[:30]:
        layer.trainable = False

    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(1, activation='sigmoid')
    ])

    model.compile(
        optimizer=optimizers.Adam(learning_rate=0.0001),
        loss='binary_crossentropy',
        metrics=[
            metrics.BinaryAccuracy(name='accuracy'),
            metrics.Precision(name='precision'),
            metrics.Recall(name='recall')
        ]
    )

    return model

model = build_model()

train_gen = train_datagen.flow(X_train, y_train, batch_size=16)
val_gen = val_datagen.flow(X_val, y_val, batch_size=16)

history = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=80,
    verbose=1
)

# Оценка модели
loss, acc, prec, rec = model.evaluate(X_test, y_test)

print(f"Accuracy: {acc:.4f}")
print(f"Precision: {prec:.4f}, Recall: {rec:.4f}")

# Отчет
predictions = model.predict(X_test)
pred_labels = (predictions > 0.5).astype(int)

report = pd.DataFrame({
    'Filename': f_test,
    'True': y_test,
    'Predicted': pred_labels.flatten(),
    'Confidence': predictions.flatten()
})

report.to_csv(os.path.join(report_dir, 'report.csv'), index=False)

# Сохранение модели
model.save('model/trained_model.h5')

# Графики обучения
plt.figure()

plt.plot(history.history['loss'], label='Loss')
plt.plot(history.history['val_loss'], label='Val Loss')

plt.legend()
plt.savefig(os.path.join(report_dir, 'loss.png'))
plt.close()

print("Обучение завершено")