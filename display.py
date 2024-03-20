import cv2 as cv

cap = cv.VideoCapture(0)

def open_camera_display():
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    
    while True:
        ret, frame = cap.read()  # Capture frame-by-frame
    
        # Display the resulting frame
        cv.imshow('frame', frame)
        
        if cv.waitKey(1) == ord('q'):
            break

    cap.release()  # When everything done, release the capture
    cv.destroyAllWindows()