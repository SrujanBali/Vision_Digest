import cv2 as cv

camera = cv.VideoCapture(0)
camera.set(cv.CAP_PROP_FRAME_HEIGHT, 1600)
camera.set(cv.CAP_PROP_FRAME_WIDTH, 900)

def text_detection(frame) :
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    threshed_frame = cv.adaptiveThreshold(gray_frame, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, blockSize=11, C=2)

    return threshed_frame

if not camera.isOpened():
    print("Error: Couldn't open the camera")
    exit()

print("Camera accessed successfully")
print("Press \'s\' to save the image")

while True: 
    ret, frame = camera.read()

    if not ret:
        print("Error: Faiiled to grab frame")
        break

    cv.imshow("Camera Preview", frame)

    key = cv.waitKey(1) & 0xFF

    if key == ord('s'):
        filename = r"C:\Users\Srujan Bali\Documents\Srujan\Programming\Python Projects\Vision_Digest\data\processed/capturedImage.png"
        cv.imwrite(filename, frame)
        print("Image succcessfully captured and saved")
        break

    elif key == ord('t'):
        filename = r"C:\Users\Srujan Bali\Documents\Srujan\Programming\Python Projects\Vision_Digest\data\processed/thresholdimage.png"
        threshed_image = text_detection(frame)
        cv.imshow("Threshed Image", threshed_image)
        cv.imwrite(filename, threshed_image)

    elif key == ord('q'):
        print("Closing camera without saving")
        break



camera.release()
cv.destroyAllWindows()
