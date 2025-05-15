import tkinter as tk
from tkinter import filedialog, Label, Button
from PIL import Image, ImageTk
from plant_disease_classifier import PlantDiseaseClassifier

class PlantDiseaseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Plant Disease Detection")
        self.root.geometry("500x600")

        # Instruction Label
        self.image_label = Label(root, text="Upload a Plant Image", font=("Arial", 14))
        self.image_label.pack(pady=10)

        # Upload Button
        self.upload_button = Button(root, text="Upload Image", command=self.upload_image, font=("Arial", 12))
        self.upload_button.pack(pady=5)

        # Image Display
        self.img_display = Label(root)
        self.img_display.pack()

        # Predict Button (Initially Disabled)
        self.predict_button = Button(root, text="Predict", command=self.predict_disease, font=("Arial", 12), state=tk.DISABLED)
        self.predict_button.pack(pady=10)

        # Label to Show Results (Green Color)
        self.result_label = Label(root, text="", font=("Arial", 12), fg="green", wraplength=400, justify="left")
        self.result_label.pack(pady=10)

        self.image_path = None  # Store selected image path

    def upload_image(self):
        """ Opens file dialog to select an image """
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])

        if self.image_path:
            img = Image.open(self.image_path)
            img = img.resize((200, 200))  # Resize for display
            img = ImageTk.PhotoImage(img)

            self.img_display.config(image=img)
            self.img_display.image = img  # Keep a reference
            self.predict_button.config(state=tk.NORMAL)  # Enable Predict button

    def predict_disease(self):
        """ Runs disease detection on uploaded image and displays the same terminal output """
        if not self.image_path:
            self.result_label.config(text="Please upload an image first.", fg="red")
            return

        # Initialize classifier and load model
        classifier = PlantDiseaseClassifier()
        classifier.load_model('plant_disease_model.h5')

        # Make prediction
        result = classifier.predict(self.image_path)

        # Extract and fix confidence value
        confidence = result.get('confidence', 0.0)  # Default to 0.0 if missing
        try:
            confidence = float(confidence) * 100  # Convert to float and scale to percentage
        except (ValueError, TypeError):
            confidence = 0.0  # Fallback if conversion fails

        # Prepare output text
        output_text = (
            f"Plant Disease Analysis Results:\n"
            f"🌱 Plant Type: {result.get('plant_type', 'Unknown')}\n"
            f"🦠 Disease: {result.get('disease', 'Unknown')}\n"
            f"📊 Confidence: {result.get('confidence','.2f')}\n"
            f"🌿 Health Status: {'✅ Healthy' if result.get('is_healthy', False) else '❌ Diseased'}"
        )

        # Show output in GUI (Green Color)
        self.result_label.config(text=output_text, fg="green")

        # Also print to terminal for verification
        print(output_text)

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = PlantDiseaseGUI(root)
    root.mainloop()
