import cv2
from skimage.metrics import structural_similarity
import numpy as np

if __name__ == '__main__':

    crop_screenshot()
    image1 = cv2.imread(CROPPED_SCREENSHOT)
    image2 = cv2.imread(ORIGINAL_TV)
    # Convert the images to grayscale
    gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    w, h = gray_image2.shape[::-1]

    # Match the template (original image) within the screenshot
    result = cv2.matchTemplate(gray_image1, gray_image2, cv2.TM_CCOEFF_NORMED)

    # Define a threshold for similarity
    similarity_threshold = 0.2  # Adjust this threshold as needed

    # Find the locations where the similarity score is greater than the threshold
    locations = np.where(result > similarity_threshold)

    if len(locations) > 0:
        print('The original image (or something very similar) is present in the screenshot.')
    else:
        print('The original image is not present in the screenshot.')

    for pt in zip(*locations[::-1]):
        cv2.rectangle(image1, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    cv2.imwrite('res.png', image1)
