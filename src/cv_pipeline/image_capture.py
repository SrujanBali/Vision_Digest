import cv2 as cv

def get_threshed(frame) :
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    blur_frame = cv.GaussianBlur(gray_frame, (3, 3), 0)

    threshed_frame = cv.adaptiveThreshold(blur_frame, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, blockSize=7, C=2)

    return threshed_frame

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
        h, w = frame.shape[:2]

        if w != cam_width or h != cam_height:
            frame = cv.resize(frame, (cam_height, cam_width), interpolation=cv.INTER_AREA)

        if not ret:
            print("Error: Faiiled to grab frame")
            break

        cv.imshow("Camera Preview", frame)

        key = cv.waitKey(1) & 0xFF

        if key == ord('s'):
            filename = r"C:\Users\Srujan Bali\Documents\Srujan\Programming\Python Projects\Vision_Digest\data\processed\capturedImage.png"
            cv.imwrite(filename, frame)
            print("Image succcessfully captured and saved")
            break

        elif key == ord('t'):
            filename = r"C:\Users\Srujan Bali\Documents\Srujan\Programming\Python Projects\Vision_Digest\data\processed\thresholdimage.png"
            threshed_image = get_threshed(frame)
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

