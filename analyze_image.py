from database import Database
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import os


def analyze_image(image_path):
    db = Database()

    # Создаём анализ
    analysis_id = db.create_analysis()

    # Добавляем изображение
    image_id = db.add_image(
        analysis_id,
        filename=os.path.basename(image_path),
        path=image_path
    )

    # Добавляем объект
    object_id = db.add_object("Object", "Detected object")

    model = load_model('model/trained_model.h5')

    image = cv2.imread(image_path)
    image = cv2.resize(image, (224, 224))
    image = image / 255.0

    prediction = model.predict(np.expand_dims(image, axis=0))[0][0]

    if prediction > 0.5:
        db.add_result(
            image_id=image_id,
            object_id=object_id,
            x=112,
            y=112,
            probability=float(prediction),
            fragment_path=image_path
        )

    print("Анализ завершён")