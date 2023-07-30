import time
import cv2
import numpy as np

def capture_img(name_path):
	"""
	It captures the image then crops it to extract just the square of legos.
	:param name_path: String, the absolute path + name of the picture (or just name like "test.jpg")
	:return:  returns the cropped image
	"""

	# Open the webcam (use the appropriate index for your webcam, 0 for the first webcam)
	cap = cv2.VideoCapture(0)
	
	# Check if the webcam is opened successfully
	if not cap.isOpened():
		print("Error: Unable to access the webcam.")
		return None
	
	# Add a small delay to stabilize the camera
	#time.sleep(2)
	
	# Read a frame from the webcam
	ret, image = cap.read()
	
	cv2.imwrite(name_path, image)
	
	
	# Release the webcam capture object
	cap.release()
	
	if not ret:
		print("Error: Failed to capture an image from the webcam.")
		return None

	image = cv2.imread(name_path)

	# Convert the image to grayscale to get rid of colors and their confusion
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# Threshold the image to create a mask based on the grayscale interval [120,255]
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
	cropped_image = result[y:y+h, x:x+w]

	# Save the cropped image
	cv2.imwrite("result.jpg", cropped_image)
    
    # print(type(cropped_image))

	# Display the original and cropped images (optional)
	# cv2.imshow("Original Image", image)
    # =============================================================================
    # 	cv2.imshow("Cropped Image", cropped_image)
    # 	cv2.waitKey(0)
    # 	cv2.destroyAllWindows()
    # =============================================================================

	return cropped_image

# For testing, capture an image from the webcam and save it as "original.jpg"
#capture_img("original.jpg")
