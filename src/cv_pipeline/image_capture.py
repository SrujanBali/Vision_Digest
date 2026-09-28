import cv2

camera = cv2.VideoCapture(1)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 900)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1600)

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

    cv2.imshow("Camera Preview", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        filename = r"C:\Users\Srujan Bali\Documents\Srujan\Programming\Python Projects\Vision_Digest\data\processed/capturedImage.png"
        cv2.imwrite(filename, frame)
        print("Image succcessfully captured and saved")
        break

    elif key == ord('q'):
        print("Closing camera without saving")
        break

camera.release()
cv2.destroyAllWindows()
