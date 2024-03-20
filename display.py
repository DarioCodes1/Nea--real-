import cv2 as cv
cap = cv.VideoCapture(0) # Open the default camera (index 0)

# Function to open camera display
def open_camera_display():
    # Check if camera is opened successfully
    if not cap.isOpened():
        print("Cannot open camera")
        exit()  # Exit the program if camera cannot be opened
    
    # Loop to continuously capture frames from the camera
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        # Display the resulting frame
        cv.imshow('frame', frame)
        
        # Break the loop if 'q' key is pressed
        if cv.waitKey(1) == ord('q'):
            break
    
    # Release the camera capture object when loop is exited
    cap.release()
    
    # Close all OpenCV windows
    cv.destroyAllWindows()
