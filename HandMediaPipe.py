import cv2
import imutils
import mediapipe as mp
from imutils.video import WebcamVideoStream

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


# For webcam input:
cap = WebcamVideoStream(src=0).start()
with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.8,
        max_num_hands=2) as hands:

    while cap.stream.isOpened():

        success, image = cap.grabbed, cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image = imutils.resize(image, width=1024)
        image.flags.writeable = False
        results = hands.process(image)
        print(results.multi_hand_landmarks)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
cv2.destroyAllWindows()
cap.stop()

