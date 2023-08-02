# import picamera    # Library needed to operate the Picamera
import time
import cv2
import numpy as np


def capture_img(name_path):
	"""
		It captures the image then cropps it to extract just the square of legos.
		:param name_path: String, the absolute path + name of the picture (or just name like "test.jpg")
		:return:  returns the cropped image
	"""

	# camera = picamera.PiCamera()  # Initialise the camera
	time.sleep(2)  # Add a small delay to stop fidgeting
	# camera.capture(name_path)     # Capture the picture and save it following that path+name

	'''
	Leaving this here (the live feed then take a picture thingie)
	 just for when we need it for testing before we get the stand done
	        try:
	                # Start the live feed
	                camera.start_preview()

	                # Wait for the user to press "enter"
	                input("Press 'Enter' to capture an image...")

	                # Capture an image
	                camera.capture(path_img)
	        finally:
	                # Stop the live feed
	                camera.stop_preview()
	'''

	# Load the image
	image = cv2.imread(name_path)

	# Convert the image to grayscale to get rid of colours and their confusion
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
	cropped_image = result[y:y + h, x:x + w]

	## Display the original and cropped images
	# cv2.imshow("Original Image", image)
	# cv2.imshow("Cropped Image", cropped_image)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()

	return cropped_image

## for test if needed
# capture_img("original.jpg")