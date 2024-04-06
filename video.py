import cv2


def camera():
    # Open the camera
    cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    # Get the default resolutions
    frame_width = int(cam.get(3))
    frame_height = int(cam.get(4))

    # Define the codec using VideoWriter_fourcc and create a VideoWriter object
    # We specify output file name "output.mp4", codec "mp4v", FPS as 30.0, and frame size as (frame_width, frame_height)
    out = cv2.VideoWriter(
        "output.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 30.0, (frame_width, frame_height)
    )

    while True:
        ret, frame = cam.read()
        if ret == True:
            # Write the frame to the output file
            out.write(frame)

            # Display the resulting frame (optional)
            cv2.imshow("Frame", frame)

            # Break the loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            break

    # Release the camera and writer, destroy all windows
    cam.release()
    out.release()
    cv2.destroyAllWindows()


camera()
