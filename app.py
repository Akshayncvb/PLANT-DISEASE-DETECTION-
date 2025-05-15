from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np

# Load the trained model
model = load_model(r'C:\plant\plant_disease_model.h5')

# Path to your test dataset
test_data_dir = 'C:\plant\test'  # Update this with the actual path

# Data preprocessing for test images
test_datagen = ImageDataGenerator(rescale=1./255)

test_generator = test_datagen.flow_from_directory(
    test_data_dir,
    target_size=(224, 224),  # Adjust to your model's input size
    batch_size=32,
    class_mode='categorical',  # Change to 'binary' if only two classes
    shuffle=False
)

# Evaluate the model
loss, accuracy = model.evaluate(test_generator)

print(f"Test Accuracy: {accuracy * 100:.2f}%")
print(f"Test Loss: {loss:.4f}")
