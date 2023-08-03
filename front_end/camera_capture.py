import cv2
import time
import numpy as np
from PIL import ImageTk, Image

class Camera:
    def __init__(self):
        # Initialize the camera capture object
        self.camera = cv2.VideoCapture(0)

        # Check if the camera was successfully opened
        if not self.camera.isOpened():
            raise RuntimeError("Failed to open the camera.")

    def __del__(self):
        # Release the camera when the object is deleted
        if self.camera.isOpened():
            self.camera.release()

    def is_opened(self):
        # Check if the camera is opened
        return self.camera.isOpened()

    def capture_img_new(self, name_path):
        # Check if the webcam is opened successfully
        if not self.camera.isOpened():
            print("Error: Unable to access the webcam.")
            return None
        start_time = time.time()

        # Add a small delay to stabilize the camera (you can uncomment this if needed)
        # time.sleep(2)

        # Read a frame from the webcam
        ret, image = self.camera.read()
        
        
        if not ret:
            print("Error: Failed to capture an image from the camera.")
        elif image is None or image.size == 0:
            print("Error: Captured image is empty or invalid.")
        else:
            # Valid image data, now try to write it to a file
            try:
                cv2.imwrite(name_path, image)
                print(f"Image saved successfully as '{name_path}'.")
            except Exception as e:
                print(f"Error occurred while writing the image: {e}")


        # Save the image to the specified file path
        cv2.imwrite(name_path, image)

        if not ret:
            print("Error: Failed to capture an image from the webcam.")
            return None

        # Convert the image to grayscale to get rid of colors and their confusion
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Threshold the image to create a mask based on the grayscale interval [120, 255]
        _, mask = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find the largest contour (the Lego square) based on its area
        largest_contour = max(contours, key=cv2.contourArea)

        # Create a mask for the largest contour
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.drawContours(mask, [largest_contour], -1, (255), thickness=cv2.FILLED)

        # Bitwise-and the mask with the original image to remove the background
        result = cv2.bitwise_and(image, image, mask=mask)

        # Find the bounding box coordinates of the contour
        x, y, w, h = cv2.boundingRect(largest_contour)

        # Crop the image to the region of interest
        cropped_image = result[y:y + h, x:x + w]

        # Save the cropped image
        cv2.imwrite("result.jpg", cropped_image)
        
        end_time = time.time()

        # Calculate the elapsed time
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time} seconds")
        
        dummy = Image.open('result.jpg')
        cropped_image = ImageTk.PhotoImage(dummy)

        return cropped_image