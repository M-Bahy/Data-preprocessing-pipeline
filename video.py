import cv2
import keyboard

def record(path):
    # Open the camera
    cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    # Get the default resolutions
    frame_width = int(cam.get(3))
    frame_height = int(cam.get(4))

    # Define the codec using VideoWriter_fourcc and create a VideoWriter object
    # We specify output file name "output.mp4", codec "mp4v", FPS as 30.0, and frame size as (frame_width, frame_height)
    out = cv2.VideoWriter(
        "path.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 15.0, (frame_width, frame_height)
    )
    print("Recording...")
    while True:
        ret, frame = cam.read()
        if ret == True:
            # Write the frame to the output file
            out.write(frame)

            # Display the resulting frame (optional)
            #cv2.imshow("Frame", frame)

            # Break the loop on 'q' key press
            if keyboard.is_pressed('esc'):
                print("Recording stopped.")
                break
        else:
            break

    # Release the camera and writer, destroy all windows
    cam.release()
    out.release()
    cv2.destroyAllWindows()