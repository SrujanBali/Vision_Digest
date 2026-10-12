# Test your Image Capture settings and functionalities over here!!

import cv2 as cv
from .easyOCR_extraction import easyocr_text_extraction
from .tesseract_extraction import get_preprocessed_threshed

def cv_main(cam_width = 1280, cam_height = 720):
    camera = cv.VideoCapture(0)
    camera.set(cv.CAP_PROP_FRAME_HEIGHT, cam_height)
    camera.set(cv.CAP_PROP_FRAME_WIDTH, cam_width)


    if not camera.isOpened():
        print("Error: Couldn't open the camera")
        exit()

    print("Camera accessed successfully")
    print("Press 's' to save the image")
    print("Press 't' to threshold and save")
    print("Press 'q' to quit")

    while True: 
        ret, frame = camera.read()

        if not ret:
            print("Error: Faiiled to grab frame")
            break

        cv.imshow("Camera Preview", frame)

        key = cv.waitKey(1) & 0xFF

        if key == ord('s'):
            filename = r"C:\Users\Srujan Bali\Documents\Srujan\Programming\Python Projects\Vision_Digest\data\processed\capturedImage.png"
            cv.imwrite(filename, frame)
            text_extracted = easyocr_text_extraction(frame)
            print(text_extracted)
            print("Image succcessfully captured and saved")
            break

        elif key == ord('p'):
            filename = r"C:\Users\Srujan Bali\Documents\Srujan\Programming\Python Projects\Vision_Digest\data\processed\thresholdimage.png"
            threshed_image = get_preprocessed_threshed(frame)
            cv.imwrite(filename, threshed_image)
            print("Threshed Image saved successfully")
            cv.imshow("Threshed Image", threshed_image)
            break

        elif key == ord('q'):
            print("Closing camera without saving")
            break


    camera.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    cv_main()